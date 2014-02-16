# -*- coding: utf-8 -*-
"""
core.views
"""

import logging

from google.appengine.api import users
from google.appengine.api import memcache
from werkzeug import (
    unescape, redirect, Response,
)
from werkzeug.exceptions import (
    NotFound, MethodNotAllowed, BadRequest
)

from kay.utils import (
    render_to_response, reverse,
    get_by_key_name_or_404, get_by_id_or_404,
    to_utc, to_local_timezone, url_for, raise_on_dev,
    create_login_url,
)
from kay.i18n import gettext as _
from kay.auth.decorators import admin_required
from kay import handlers
from kay.utils.flash import (
    set_flash, get_flash
)
from kay.utils.decorators import retry_on_timeout

import models
import forms
import settings

# Create your views here.

@retry_on_timeout(retries=3)
def save_tweet(request):
    code = request.session.get('code', '')
    message = request.session.get('message', '')
    tweet = models.Tweet(code=code, message=message)
    tweet.put()
    return tweet


def url_for_tweet(tweet, external=True):
    return url_for('core/show', id=tweet.key().id(), _external=external)


def post_tweet(request, tweet):
    from google.appengine.api import urlfetch
    from django.utils import simplejson
    import oauth

    message = "%s %s" % (tweet.message, url_for_tweet(tweet))
    
    access_token = request.user.raw_user_data['access_token']
    key = access_token['key']
    secret = access_token['secret']
    params = {"status": message.lstrip() }
    url = 'http://twitter.com/statuses/update.json'

    client = oauth.TwitterClient(
        settings.GAEMA_SECRETS['twitter_consumer_key'],
        settings.GAEMA_SECRETS['twitter_consumer_secret'],
        None)

    response = client.make_request(url=url, token=key, secret=secret,
        additional_params=params, protected=True, method=urlfetch.POST)

    data = simplejson.loads(response.content)
    if data.has_key('error'):
        set_flash(data['error']) 
    else:
        set_flash(u'コードスニペットを Twitter でつぶやきました。')

    request.session.pop('code')
    request.session.pop('message')

    return response


class IndexHandler(handlers.BaseHandler):
    def prepare(self):
        self.form = forms.TweetForm()

    def get(self):
        return render_to_response('core/index.html', {
            'form': self.form.as_widget(),
        })
  
    def post(self):
        if self.form.validate(self.request.form):
            self.request.session['code'] = self.form['code']
            self.request.session['message'] = self.form['message']
            if self.request.user.is_anonymous():
                callback = url_for('core/post', _external=True)
                return redirect(create_login_url(callback))
            else:
                tweet = save_tweet(self.request)
                post_tweet(self.request, tweet)
                return redirect(url_for_tweet(tweet))
        return self.get()


class PostTweetHandler(handlers.BaseHandler):
    def get(self):
        if self.request.user.is_anonymous():
            raise BadRequest(u'ログインしていません。')
        elif not self.request.session.has_key('code'):
            raise BadRequest(u'コードスニペットが渡されていません。')
        tweet = save_tweet(self.request)
        post_tweet(self.request, tweet)
        return redirect(url_for_tweet(tweet))


class ShowHandler(handlers.BaseHandler):
    def get(self, id):
        tweet = get_by_id_or_404(models.Tweet, id)
        return render_to_response('core/show.html', {
            'tweet': tweet,
            'message': get_flash()
        })


index = IndexHandler()
show = ShowHandler()
post = PostTweetHandler()


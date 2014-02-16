# -*- coding: utf-8 -*-
# core.models

from google.appengine.ext import db
from kay.db import OwnerProperty
from kay.ext.gaema.models import GAEMAUser


class Tweet(db.Model):
    user = OwnerProperty()
    code = db.TextProperty(required=True)
    message = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)


class User(GAEMAUser):
    pass


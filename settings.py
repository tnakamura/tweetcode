# -*- coding: utf-8 -*-

"""
A sample of kay settings.

:Copyright: (c) 2009 Accense Technology, Inc. 
                     Takashi Matsuo <tmatsuo@candit.jp>,
                     All rights reserved.
:license: BSD, see LICENSE for more details.
"""

DEFAULT_TIMEZONE = 'Asia/Tokyo'
DEBUG = True
PROFILE = False
SECRET_KEY = 'ReplaceItWithSecretString'
SESSION_PREFIX = 'gaesess:'
COOKIE_AGE = 1209600 # 2 weeks
COOKIE_NAME = 'KAY_SESSION'

ADD_APP_PREFIX_TO_KIND = True

ADMINS = (
)

TEMPLATE_DIRS = (
)

USE_I18N = False
DEFAULT_LANG = 'en'

INSTALLED_APPS = (
    'kay.sessions',
    'kay.ext.gaema',
    'core',
)

APP_MOUNT_POINTS = {
    'core': '/'
}

MIDDLEWARE_CLASSES = (
    'kay.auth.middleware.AuthenticationMiddleware',
    'kay.sessions.middleware.SessionMiddleware',
    'kay.utils.flash.FlashMiddleware',
)

SESSION_STORE = 'kay.sessions.sessionstore.GAESessionStore'

AUTH_USER_BACKEND = 'kay.auth.backends.gaema.GAEMABackend'
GAEMA_USER_MODEL = 'core.models.User'

GAEMA_SECRETS = {
    'twitter_consumer_key': '',
    'twitter_consumer_secret': '',
}

GAEMA_VALID_SERVICES = [
    'twitter',
]

# You can remove following settings if unnecessary.
CONTEXT_PROCESSORS = (
  'kay.context_processors.request',
  'kay.context_processors.url_functions',
  'kay.context_processors.media_url',
)

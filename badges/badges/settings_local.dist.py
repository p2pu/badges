from settings import *

# conf for django debug toolbar
DEBUG = True
INSTALLED_APPS += ( 'debug_toolbar',)
MIDDLEWARE_CLASSES += ( 'debug_toolbar.middleware.DebugToolbarMiddleware',)
INTERNAL_IPS = ('127.0.0.1', )
DEBUG_TOOLBAR_CONFIG = { 'INTERCEPT_REDIRECTS': False }

INSTALLED_APPS += ( 'testdata', )

OAUTH_GRANT_URL = 'http://host.org/oauth/authorize/'
OAUTH_TOKEN_URL = 'http://host.org/oauth/token/'
OAUTH_CLIENT_ID = ''
OAUTH_CLIENT_KEY = ''
OAUTH_CLIENT_SECRET = ''
OAUTH_ID_URL = 'http://host.org/oauth/whoami/'

LERNANTA_API_KEY = ''
NOTIFICATION_URL = 'https://host.org/notification/url/'

DEFAULT_FROM_ADDRESS = 'Admin'

OPEN_BADGES_PUBLIC_URL = 'http://localhost:8000'
OPEN_BADGES_ORGANISATION_NAME = 'P2PU Org.'
OPEN_BADGES_ORGANISATION_URL = 'https://www.p2pu.org'
OPEN_BADGES_HASH_EMAIL_SALT = 'alivesea'

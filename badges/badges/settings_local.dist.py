from settings import *

# conf for django debug toolbar
INSTALLED_APPS += ( 'debug_toolbar',)
MIDDLEWARE_CLASSES += ( 'debug_toolbar.middleware.DebugToolbarMiddleware',)
INTERNAL_IPS = ('127.0.0.1', )

OAUTH_GRANT_URL = 'http://host.org/oauth/authorize/'
OAUTH_TOKEN_URL = 'http://host.org/oauth/token/'
OAUTH_CLIENT_ID = ''
OAUTH_CLIENT_KEY = ''
OAUTH_CLIENT_SECRET = ''
OAUTH_ID_URL = 'http://host.org/oauth/whoami/'
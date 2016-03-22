# Django settings for badges project.
import os
import sys

DEBUG = False
TEMPLATE_DEBUG = DEBUG
PROJECT_DIR = os.path.dirname(__file__)
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': path('db.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
ALLOWED_HOSTS = [
    '.p2pu.org'
]
TIME_ZONE = 'Europe/Amsterdam'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False

MEDIA_ROOT = path('../uploads')
MEDIA_URL = '/media/'
STATIC_ROOT = path('../staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, '../static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

LANGUAGE_CODE = 'en-us'

gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('en-us', gettext('English-American')),
)

SECRET_KEY = '(auvykgyxsa=bv16j75p_p90jqx%d54)u=ilx2m0id-g-vg+eh'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'open_badges.context_processors.process',
)

ROOT_URLCONF = 'badges.urls'

WSGI_APPLICATION = 'badges.wsgi.application'

TEMPLATE_DIRS = (
    path('../templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'south',
    'crispy_forms',
    'parsley',
    'compressor',
    'landing',
    'dashboard',
    'badge',
    'project',
    'media',
    'oauthclient',
    'open_badges',
    'notifications',
    'p2pu_user',
    'oembed',
)

#############################################################################
# Logging settings
#############################################################################
from django.core.exceptions import SuspiciousOperation


def skip_suspicious_operations(record):
    if record.exc_info:
        exc_value = record.exc_info[1]
        if isinstance(exc_value, SuspiciousOperation):
            return False
    return True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'skip_suspicious_operations': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_suspicious_operations,
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': path('badges.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#############################################################################
# OAuth settings
#############################################################################

OAUTH_GRANT_URL = ''
OAUTH_TOKEN_URL = ''
OAUTH_CLIENT_ID = ''
OAUTH_CLIENT_KEY = ''
OAUTH_CLIENT_SECRET = ''
OAUTH_ID_URL = ''
LERNANTA_API_KEY = ''
NOTIFICATION_URL = 'https://host.org/notification/url/'

##################################################################
# Django compressor settings
#################################################################
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
)

##################################################################
# Open badges settings
#################################################################
OPEN_BADGES_ISSUER_JS_URL = '//backpack.openbadges.org/issuer.js'

##################################################################
# Crispy forms template
#################################################################
CRISPY_TEMPLATE_PACK = 'bootstrap'

##################################################################
# Embedding settings
#################################################################
ORGANISATION_URL = 'badges.p2pu.org'

##################################################################
# Testing mode
#################################################################
DEFAULT_FROM_EMAIL = "badges@p2pu.org"

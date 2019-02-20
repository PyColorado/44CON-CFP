import os
from pathlib import Path

import environ

import django_heroku
import dj_database_url


#############
# CONSTANTS #
#############

root = environ.Path(__file__) - 1
BASE_DIR = Path(root())
ENVIRONMENT = os.environ.get('ENVIRONMENT', default='development')
DEBUG = os.environ.get('DEBUG', default=False)
SECRET_KEY = os.environ.get('SECRET_KEY')
USE_DJANGO_HIJACK = os.environ.get('USE_DJANGO_HIJACK', default=True)
USE_MINIFICATION = os.environ.get('USE_MINIFICATION', default=True)
DATABASE_URL = os.environ.get('DATABASE_URL')
DEBUG_TOOLBAR = os.environ.get('DEBUG_TOOLBAR', default=False)
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDGRID_SENDER_DOMAIN = os.environ.get('SENDGRID_SENDER_DOMAIN')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

CONFERENCE_NAME = os.environ.get('CONFERENCE_NAME')
CONFERENCE_YEAR = os.environ.get('CONFERENCE_YEAR')
CONFERENCE_EMAIL = os.environ.get('CONFERENCE_EMAIL')
CONFERENCE_URL = os.environ.get('CONFERENCE_URL')

CSRF_FAILURE_VIEW = "gambit.views.csrf_failure"
ROOT_URLCONF = "gambit.urls"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
WSGI_APPLICATION = "gambit.wsgi.application"
MINIMUM_PASSWORD_LENGTH = 12
# Whitelist of acceptable file types for submissions
CONTENT_TYPES = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-powerpoint',
    'application/zip',
    'application/x-zip',
    'application/octet-stream',
    'application/x-zip-compressed',
]
MAX_UPLOAD_SIZE = 52428000 #50MiB

if ENVIRONMENT == 'production':
    SECURE_HSTS_SECONDS = 3600
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SSL_REQUIRED = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    ALLOWED_HOSTS = [
        '.herokuapp.com',
    ]
else:
    ALLOWED_HOSTS = ['*']
    SSL_REQUIRED = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False


##########################
# Application definition #
##########################

INSTALLED_APPS = [
    'gambit.apps.GambitConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'anymail',
    'django_unused_media',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'gambit.context_processors.global_settings',
            ],
        },
    },
]


###########
# Logging #
###########

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format':   '%(levelname)s %(asctime)s %(module)s '
                        '%(process)d %(thread)d %(message)s',
        },
        'coloured_verbose': {
            '()': 'colorlog.ColoredFormatter',
            'format': "%(log_color)s%(levelname)s %(bold_white)s[%(process)d] %(bold_blue)s%(message)s",
        },
    },
    'handlers': {
        'coloured_console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'coloured_verbose',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['coloured_console'],
        },
        'gunicorn.access': {
            'handlers': ['coloured_console'],
        },
        'gunicorn.error': {
            'handlers': ['coloured_console'],
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['coloured_console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['coloured_console'],
            'propagate': False,
        },
    },
}


#########
# Cache #
#########

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


#######################
# Password validation #
#######################

PASSWORD_HASHERS = [
    'gambit.hashers.ParanoidBCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': MINIMUM_PASSWORD_LENGTH,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]


########################
# Internationalization #
########################

LANGUAGE_CODE = "en-us"
TIME_ZONE = 'America/Denver'
USE_I18N = True
USE_L10N = True
USE_TZ = True


###############
# STATICFILES #
###############

STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, os.path.join(os.pardir, "bower_components")),
    os.path.join(BASE_DIR, "assets"),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]


################
# Minification #
################

if USE_MINIFICATION:
    MIDDLEWARE.append("htmlmin.middleware.HtmlMinifyMiddleware")
    MIDDLEWARE.append("htmlmin.middleware.MarkRequestMiddleware")
    HTML_MINIFY = True
    INSTALLED_APPS.append("compressor")
    COMPRESS_OUTPUT_DIR = 'cache'
    COMPRESS_OFFLINE = False
    COMPRESS_ENABLED = True


#################
# Django Hijack #
#################

# https://github.com/arteria/django-hijack

if USE_DJANGO_HIJACK:
    INSTALLED_APPS.append("hijack")
    INSTALLED_APPS.append("hijack_admin")
    INSTALLED_APPS.append("compat")
    HIJACK_LOGIN_REDIRECT_URL = "/profile/"
    HIJACK_LOGOUT_REDIRECT_URL = "/admin/auth/user/"
    HIJACK_USE_BOOTSTRAP = True
    HIJACK_ALLOW_GET_REQUESTS = True


#################
# Debug Toolbar #
#################

if DEBUG_TOOLBAR:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(3, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ['127.0.0.1', 'localhost']


#########
# Email #
#########

if ENVIRONMENT == 'production':
    EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
    ANYMAIL = {
        'SENDGRID_API_KEY': SENDGRID_API_KEY,
        'SENDGRID_SENDER_DOMAIN': SENDGRID_SENDER_DOMAIN,
    }
    DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL
else:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")


##########
# Heroku #
##########

# Configure Django App for Heroku.
# should be placed at the very bottom of settings.py
# https://github.com/heroku/django-heroku#usage-of-django-heroku

django_heroku.settings(locals())


############
# Database #
############

# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
  'default': dj_database_url.config(default=DATABASE_URL)
}
locals()['DATABASES']['default'] = dj_database_url.config(ssl_require=SSL_REQUIRED)

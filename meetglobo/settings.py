"""
Django settings for rh project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from django.conf import global_settings
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',
                    "django.template.loaders.app_directories.Loader",)
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nu+uk5#hp#qm9c-^$7n)0yjv_s$7v0n6$9uu-ko3c9z&jk)!k_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
PROJECT_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
TEMPLATE_DEBUG = True
def rel(*x):
    return os.path.abspath(os.path.join(PROJECT_ROOT, *x))
TEMPLATE_DIRS = (
                    rel("templates/"),
                )

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'page',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 180 * 60  # The user sessions expires in 3hs.
ROOT_URLCONF = 'meetglobo.urls'

WSGI_APPLICATION = 'meetglobo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

DATE_INPUT_FORMATS = ('%M %d, %Y')

LANGUAGE_CODE = 'es-uy'

TIME_ZONE = 'America/Montevideo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = rel('assets')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
                    rel('static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',)
MEDIA_ROOT = rel('media')
MEDIA_URL = '/media/'
MEDIA_BUCKET = None
MEDIA_LOCATION = None
MEDIA_DOMAIN = None
MEDIA_HEADERS = {
    'Expires': 'Thu, 31 Dec 2050 00:00:00 GMT',
    'Cache-Control': 'max-age=315360000, public'
}
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


LOGIN_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Host for sending e-mail.
EMAIL_HOST = 'localhost'

# Port for sending e-mail.
EMAIL_PORT = 1025

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
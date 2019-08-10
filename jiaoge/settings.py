"""
For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os

import environ  # django-environ for 12-factor app compatible settings.


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WSGI_APPLICATION = 'jiaoge.wsgi.application'
ROOT_URLCONF = 'jiaoge.urls'

# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Keep media files separately from static files.
DEFAULT_FILE_STORAGE = 'jiaoge.storage.S3MediaStorage'
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# For filesystem finder (global statics).
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'storages',
    'django_countries',

    'users',
    'postcards',
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
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]

# https://docs.djangoproject.com/en/2.2/topics/auth/customizing/
# #specifying-custom-user-model
AUTH_USER_MODEL = 'users.User'

# PARSED FROM ENVIRONMENT #
env = environ.Env()  # Parser for env-sourced configuration.

DEBUG = env('DEBUG', cast=bool, default=False)
SECRET_KEY = env('SECRET_KEY')
HASHID_FIELD_SALT = env('HASHID_FIELD_SALT')  # Salt for hashids lib.
ADMIN_URL = env('ADMIN_URL')

# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': env.db(),
}

ALLOWED_HOSTS = [
    env('HEROKU_DOMAIN', default=None)
]

# Static file config.
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default=None)
AWS_DEFAULT_ACL = env('AWS_DEFAULT_ACL', default=None)
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default=None)
AWS_LOCATION = env('AWS_LOCATION', default='static')
AWS_S3_FILE_OVERWRITE = env('AWS_S3_FILE_OVERWRITE', default=True)
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

"""
Django settings for talentalps project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import config, Csv
import logging.config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(post_process=tuple), default="127.0.0.1")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # Additional Django apps
    'django.contrib.postgres',
    'sass_processor',
    'widget_tweaks',
    'storages',
    'boto3',
    'ckeditor',

    # Project apps
    'talentalps',
    'cms',
    'user',
    'employer',
    'registration',
    'job',
    'notifications',
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

AUTHENTICATION_BACKENDS = [
    'user.auth_backend.UserProfileBackend',
]

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

ROOT_URLCONF = 'talentalps.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
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

WSGI_APPLICATION = 'talentalps.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': config('DB_HOST', default=""),
        'PORT': config('DB_PORT', default=""),
        'NAME': config('DB_NAME', default="talentalps"),
        'USER': config('DB_USER', default="talentalps"),
        'PASSWORD': config('DB_PASS', default=""),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/


# Logging Configuration

# Clear prev config
LOGGING_CONFIG = None

# Get loglevel from env
LOGLEVEL = config('DJANGO_LOGLEVEL', default='info').upper()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        'root': {
            'level': LOGLEVEL,
            'handlers': ['console',],
        },
    },
})

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=587)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
EMAIL_TIMEOUT = config('EMAIL_TIMEOUT', default=None)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default="TalentAlps Team <noreply@talentalps.my>")

# CKEDITOR SETTINGS
CKEDITOR_CONFIGS = {
    'job_listing_editor': {
        'toolbar': [["Bold", "Italic", "Strike"],
                ['NumberedList', 'BulletedList', "Indent", "Outdent", 'JustifyBlock'],
                ["SectionLink", "Subscript", "Superscript"], ['Undo', 'Redo']],
    },
}

# SASS SETTINGS
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'public/static/')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

SASS_PROCESSOR_ENABLED = True

SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, "public/static")

SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join(BASE_DIR, 'extra-styles/scss'),
    os.path.join(BASE_DIR, 'node_modules'),
]

from django.contrib.messages import constants as messages

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3zjkc0dd^5hi@xgvrkb^ip6l=$15pf)w5*spd$9dxx#0$fijf5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.medisync.friskytech.com.ng', 'medisync.friskytech.com.ng']


# Application definition

INSTALLED_APPS = [
    'formtools',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    'django_filters',
    'django.contrib.humanize',
    'mathfilters',


    # myapps
    'accounts',
    'appointments',
    'bills',
    'diagnosis',
    'locations',
    'labs',
    'medical_services',
    'patients',
    'pharmacy',
    'radiology',
    'reports',
    'visits',
    'vitals',
]

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# opional, as this will log you out when browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 900                   # 0r 5 * 60, same thing
# Will prrevent from logging you out after 300 seconds
SESSION_SAVE_EVERY_REQUEST = True


LOGOUT_REDIRECT_URL = '/login/'
ROOT_URLCONF = 'emr.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'emr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': "emr",
#         'USER': "root",
#         'PASSWORD': "",
#         'HOST': "localhost",
#         'PORT': "3306",
#     }
# }


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

DATE_FORMAT = "Y-m-d"

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/img/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'assets', 'img')
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'static_root')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    STATIC_DIR,
)


MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
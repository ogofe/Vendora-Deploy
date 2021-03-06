"""
Django settings for vendora project.

Generated by 'django-admin startproject' using Django 2.2.14.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ae1#%d3-8#v3dy_+v+c5_!16njdfp57q)ln5z*@l0i=dv8*(wp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*',
]


# Application definition

INSTALLED_APPS = [
    # vendora
    'accounts',
    'api',
    'intro',
    'plugins',
    'store',
    'vendor',
    # django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third parties
    'rest_framework',
    'corsheaders',
    # 'django_hosts',
]

MIDDLEWARE = [
    # 'django_hosts.middleware.HostsRequestMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'store.middleware.CartFetchMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # vendora middleware
    # 'store.middleware.StoreTemplateMiddleware',
    # 'django_hosts.middleware.HostsResponseMiddleware'   # must be the last!
]

ROOT_URLCONF = 'vendora.urls'

# DJANGO HOSTS
# ROOT_HOSTCONF = 'hosts.hosts'

# PARENT_HOST = 'localhost'
# # PARENT_HOST = 'vendora.com'

# DEFAULT_HOST = 'intro'

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, r'^templates/store/\*[A-Za-z0-9_]\*'),
            os.path.join(BASE_DIR, 'templates/store'),
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins':[
                # 'django_hosts.templatetags.hosts_override',
            ]
        },
    },
]

WSGI_APPLICATION = 'vendora.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_THOUSAND_SEPARATOR = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# MEDIA (Uploaded Content)

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'

# PASSWORD_RESET_TIMEOUT_DAYS
PASSWORD_RESET_TIMEOUT_DAYS = 3

# SESSION AND COOKIES
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"


CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:8100',
    'http://127.0.0.1:3000',
    'http://localhost:3000',
]

#CORS_ORIGIN_ALLOW_ALL = True


# LOGIN_REDIRECT_VIEW = 'accounts:super-in'
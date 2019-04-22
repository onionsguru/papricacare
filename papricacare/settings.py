"""
Django settings for papricacare project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o1g#kbfwe=q(+tr&z4&_!(vn*fk-u7)917jyqbozc15%wb$3be'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

run_message = None
try:
    host_name = os.environ['papricacare_host']
except KeyError:
    host_name = None

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
if host_name != None and host_name not in ALLOWED_HOSTS: # when remotely running
    ALLOWED_HOSTS.append(host_name)
    is_hosted = True
    run_message = f'<Papricacare allowed at "{host_name}",'
else: 
    run_message = f'<Papricacare run locally, '
    is_hosted = False
     
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'drug.apps.DrugConfig',
    'chat.apps.ChatConfig',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.kakao',
    
    'channels',
    'accounts.apps.AccountsConfig',
    'rest_framework',
    'ocr.apps.OcrConfig',
    'hospital',
    'disease',
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

ROOT_URLCONF = 'papricacare.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'papricacare.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

try:
    db_endpoint = os.environ['papricacare_db_host']
except KeyError:
    db_endpoint = '127.0.0.1' 
run_message = run_message + f'Postgre run at "{db_endpoint}">'
    
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'papricacare',
    'USER': 'onions',
    'PASSWORD': 'onions2018',
    'HOST': db_endpoint,
    'PORT': '5432',
    }
}


#'default': {
#    'ENGINE': 'django.db.backends.sqlite3',
#    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
LOGIN_REDIRECT_URL = '/chat/'
LOGOUT_REDIRECT_URL = '/chat/'

# for channels
ASGI_APPLICATION = "papricacare.routing.application"    
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
       "hosts":[('127.0.0.1',6379)],
        },
    }
}
STATIC_URL = '/static/'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # Django 기본 유저모델
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIAL_AUTH_URL_NAMESPACE = 'social'

LOGIN_REDIRECT_URL='/'

print(run_message)

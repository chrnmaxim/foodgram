import os

from pathlib import Path

import environ

env = environ.Env()
environ.Env.read_env('../.env')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = env.str('SECRET_KEY', default='SECRET_KEY')


DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default='localhost')


INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Сторонние библиотеки
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_yasg',
    # Приложения проекта
    'recipes.apps.RecipesConfig',
    'users.apps.UsersConfig',
    'ingredients.apps.IngredientsConfig',
    'tags.apps.TagsConfig',
    'favorite.apps.FavoriteConfig',
    'subscriptions.apps.SubscriptionsConfig',
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

ROOT_URLCONF = 'foodgram.urls'

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

WSGI_APPLICATION = 'foodgram.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('POSTGRES_DB', default='django'),
        'USER': env.str('POSTGRES_USER', 'django'),
        'PASSWORD': env.str('POSTGRES_PASSWORD', default=''),
        'HOST': env.str('DB_HOST', default=''),
        'PORT': env.int('DB_PORT', default=5432)
    }
}

AUTH_USER_MODEL = "users.User"

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


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = '/backend_static/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/media/'

CSV_DIR = os.path.join(BASE_DIR, 'data')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

DJOSER = {
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'user_list': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
        'user': ('utils.permissions.CustomPermissions',),
    },
    'SERIALIZERS': {
        'user': 'users.serializers.UserCustomSerializer',
        'current_user': 'users.serializers.UserCustomSerializer',
    },
    'LOGIN_FIELD': 'email',
}

MAX_FIELD_LENGTH: int = 255
ADMIN_CHARS_LIMIT: int = 30
PAGE_SIZE_PAGINATION: int = 5

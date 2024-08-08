from pathlib import Path

import environ

env = environ.Env()
environ.Env.read_env('../.env')

BASE_DIR = Path(__file__).resolve().parent.parent


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
    'rest_framework',
    'djoser',
    'rest_framework_simplejwt',
    'drf_yasg',
    # Приложения проекта
    'recipes.apps.RecipesConfig',
    'users.apps.UsersConfig',
    'ingredients.apps.IngredientsConfig',
    'tags.apps.TagsConfig',
    'favorite.apps.FavoriteConfig',
    'subscriptions.apps.SubscriptionsConfig'
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

USE_TZ = True


STATIC_URL = 'static/'

MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


DJOSER = {
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'user_list': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
        'user': ('foodgram.permissions.CustomPermissions',),
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

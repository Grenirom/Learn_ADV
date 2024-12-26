from decouple import config

import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG")

ALLOWED_HOSTS = []

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

ADDITIONAL_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "parler",
    "debug_toolbar",
    "django_filters",
    "knox",
    "axes",
    "taggit",
    "channels",
]

OWN_APPS = ["apps.account", "apps.posts", "apps.chat"]

INSTALLED_APPS = DJANGO_APPS + ADDITIONAL_APPS + OWN_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "apps.generals.middleware.APIVersionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "axes.middleware.AxesMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    },
    "test": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": f"test_{config('DB_NAME')}",
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "apps/account/static")]

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

AUTH_USER_MODEL = "account.CustomUser"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TAGGIT_CASE_INSENSITIVE = True


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("knox.auth.TokenAuthentication",),
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1", "v2"],
}

REST_KNOX = {
    "TOKEN_TTL": timedelta(hours=10),
    "USER_SERIALIZER": "apps.account.serializers_v1.UserSerializer",
}


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")


REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = "6379"

CELERY_BROKER_URL = "redis://" + REDIS_HOST + ":" + REDIS_PORT
CELERY_RESULT_BACKEND = "redis://" + REDIS_HOST + ":" + REDIS_PORT

# AXES SETTINGS
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "apps.generals.backends.EmailBackend",
    "axes.backends.AxesStandaloneBackend",
]


AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(minutes=5)
AXES_LOCK_OUT_AT_FAILURE = True

AXES_LOCKOUT_CALLABLE = "apps.generals.utils.custom_lockout_message"
# ToDo подумать как отображать ошибку после блокировки аккаунта в админке

# RECAPTCHA KEYS
# RECAPTCHA_PUBLIC_KEY = '6LeIP3AqAAAAAA1cIhK8IDOroQReSUmJAlTnqNJV'
# RECAPTCHA_PRIVATE_KEY = config('CAPTCHA_PRIVATE_KEY')


STRIPE_PUBLISHABLE_KEY ='pk_test_51QUKuvBznZrHg73GOXFIPcqf7TdDBpNMFKeffLoZG7Yme0H7H6VhSEffyMdxw27KsZTENQHJrCJ8TaMgpeq66EAN00zGRZk65d'
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
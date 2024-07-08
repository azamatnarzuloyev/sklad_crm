from __future__ import annotations

import logging
import logging.config
import os
from datetime import timedelta, timezone
from pathlib import Path
from environs import Env

env = Env()
env.read_env()

from .base import BASE_DIR

from .silk import SILKY_MIDDLEWARE_CLASS, USE_SILK

PROJECT_NAME = os.getenv("PROJECT_NAME", "django_template")
PROJECT_VERBOSE_NAME = os.getenv("PROJECT_VERBOSE_NAME", "Django Template").strip("'\"")


ENVIRONMENT = os.getenv("ENVIRONMENT", "local")


ALLOWED_HOSTS = ["127.0.0.1"]

DEBUG = os.environ.get("DEBUG", True)

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(" ")


INSTALLED_APPS = [
    "jazzmin",
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "debug_toolbar", 
    "django_celery_beat",
    "channels",
    "jsoneditor",
    "rest_framework",
    "django_countries",
    "django_filters",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_extensions",
    "ckeditor",
    "corsheaders",
    "axes",
    "silk",
    # local app
    "account",
    "settings",
    "cash",
    "post",
    "product",
    "category",
    "magazin",
    "puttyMagazin",
    "savdo",
    "crmuser",
    "mobileApp",
]

JSON_EDITOR_JS = "https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/8.6.4/jsoneditor.js"
JSON_EDITOR_CSS = (
    "https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/8.6.4/jsoneditor.css"
)

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
]
if DEBUG:
    INTERNAL_IPS = ["127.0.0.1"]


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

REDIS_URL = "redis://redis_broker:6379"
CHANNEL_LAYERS["default"]["CONFIG"]["hosts"] = [REDIS_URL]




MIDDLEWARE = [
  
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.midilware.errorshandler.Custom404Middleware",
     SILKY_MIDDLEWARE_CLASS,
    "axes.middleware.AxesMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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


ASGI_APPLICATION = "config.asgi.application"


LANGUAGE_CODE = "en-US"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True





SMS_TOKEN =os.environ("sms_token")
EXPIRY_TIME_OTP = 60





# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"



DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

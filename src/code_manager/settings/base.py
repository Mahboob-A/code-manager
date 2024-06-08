import os
from datetime import timedelta
from pathlib import Path

import environ

env = environ.Env()

# TODO CHANGE {ENVIRONMENT_TYPE} to PROD Environment
ENVIRONMENT_TYPE = ".dev"

# Build paths inside the project like this: ROOT_DIR / 'subdir'.
# this effectively pointing to the SRC dir where the manage.py file is located.
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# read all the dependable .env files
env.read_env(Path(str(ROOT_DIR)) / f".envs/{ENVIRONMENT_TYPE}/.django")
env.read_env(Path(str(ROOT_DIR)) / f".envs/{ENVIRONMENT_TYPE}/.postgres")

# environ.Env.read_env(
#     f"Path(__file__).resolve().parent / .envs/ {ENVIRONMENT_TYPE} / .django"
# )
# # postgres type
# environ.Env.read_env(
#     f"Path(__file__).resolve().parent / .envs / {ENVIRONMENT_TYPE} / .postgres"
# )


# apps directory
APP_DIR = ROOT_DIR / "core_apps"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_DEBUG")
if DEBUG == "True":
    DEBUG = True
else:
    DEBUG = False


# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


THIRD_PARTH_APPS = [
    "rest_framework",
    "django_filters",
    "corsheaders",
    "drf_yasg",
    "taggit",
]

LOCAL_APPS = [
    "core_apps.code_display",
    "core_apps.code_submit",
    "core_apps.code_result",
    "core_apps.common",
]

# installed apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTH_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # cors middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "code_manager.urls"

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

WSGI_APPLICATION = "code_manager.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# for testing
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": ROOT_DIR / "db.sqlite3",
#     }
# }


DATABASES = {"default": env.db("DATABASE_URL")}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

SITE_ID = 1

# admin url
ADMIN_URL = env("ADMIN_URL")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# static and media urls
STATIC_URL = "/static/"
STATIC_ROOT = str(ROOT_DIR / "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = str(ROOT_DIR / "mediafiles")


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

###############################################################

#   Rest Framework Settings
# TODO setup drf related config
REST_FRAMEWORK = {
    #     "DEFAULT_AUTHENTICATION_CLASSES": [
    #         "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    #     ],
    #     "DEFAULT_PERMISSION_CLASSES": [
    #         "rest_framework.permissions.IsAuthenticated",
    #     ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

# JWT Signing Key
JWT_SIGNING_KEY = env("JWT_SIGNING_KEY")

CORS_URLS_REGEX = r"^api/.*$"


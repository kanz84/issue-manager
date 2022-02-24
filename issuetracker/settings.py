# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position
# pylint: disable=unused-wildcard-import

"""
Django settings for issuetracker project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
PROJECT_DIR = Path(__file__).resolve().parent
BASE_DIR = PROJECT_DIR.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "i5g3&mtn!irv4!8a3a5+=&6!-ej=_42bncz@)i%z9o(x5!(3vm"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

IS_TEST = "test" in sys.argv or (len(sys.argv) > 0 and "pytest" in sys.argv[0])

LOG_FILE_LOCATION = os.path.join(BASE_DIR, "log", "app.log")

APP_NAME = "Issue Tracker"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_extensions",
    "crispy_forms",
    "rest_framework",
    "tasks.apps.TasksConfig",
]

MIDDLEWARE = [
    "log_request_id.middleware.RequestIDMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "request_logging.middleware.LoggingMiddleware",
]

ROOT_URLCONF = "issuetracker.urls"

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
                "tasks.context_processors.settings",  # Add
                "social_django.context_processors.backends",  # Add
                "social_django.context_processors.login_redirect",  # Add
            ],
        },
    },
]

WSGI_APPLICATION = "issuetracker.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "issue_manager",
        "USER": "issue_manager",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "default-character-set": "utf8",
        "PORT": "5432",
    }
}
if IS_TEST:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR.parent, "static")

CRISPY_TEMPLATE_PACK = "bootstrap4"

IS_DEBUG = False

DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)

if IS_DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + ("rest_framework.renderers.BrowsableAPIRenderer",)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        "rest_framework.permissions.IsAuthenticated",
        # 'rest_framework.permissions.AllowAny',
    ],
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10
}


env_pro = "PRO"
env_stage = "STAGE"
env_ci = "CI"
env_dev = "DEV"


def select_env():
    if os.getenv("GITHUB_WORKFLOW"):
        return env_ci
    try:
        import local_settings

        return getattr(local_settings, "env", env_dev)
    except ImportError:
        pass
    return env_dev


ENV = select_env()

if ENV == env_pro:
    from issuetracker.setting.settings_pro import *
elif ENV == env_stage:
    from issuetracker.setting.settings_stage import *
elif ENV == env_ci:
    from issuetracker.setting.settings_ci import *
elif ENV == env_dev:
    from issuetracker.setting.settings_dev import *
else:
    raise Exception("env is incorrect!")


try:
    from local_settings import *
except ImportError:
    pass


from logger import LOGGING_CONFIGURATION

LOGGING = LOGGING_CONFIGURATION

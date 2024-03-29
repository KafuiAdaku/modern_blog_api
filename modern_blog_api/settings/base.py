from pathlib import Path
import environ
from datetime import timedelta

env = environ.Env()

# Setting root dir to be same as manage.py is located
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# contains all apps of the modern blog api
APPS_DIR = ROOT_DIR / "core_apps"


# setting debug based on environment variable of prod or dev
DEBUG = env.bool("DJANGO_DEBUG", False)


# Application definition

# Default django apps
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
]

# installed third party apps for the project
THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
    "drf_yasg",
    "corsheaders",
    "djcelery_email",
    "haystack",
    "drf_haystack",
    "djoser",
    "rest_framework_simplejwt",
    "axes",
]

# created apps for blog api
LOCAL_APPS = [
    "core_apps.common",
    "core_apps.profiles",
    "core_apps.users",
    "core_apps.blogs",
    "core_apps.favorites",
    "core_apps.reactions",
    "core_apps.ratings",
    "core_apps.comments",
    "core_apps.search",
]

# combining all 3 apps into required installed app for django
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # django-axes middleware
    "axes.middleware.AxesMiddleware",
]

ROOT_URLCONF = "modern_blog_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "modern_blog_api.wsgi.application"

# Database
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# including the approved password hashing algorithm by
# django docs --> argon2
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# Redis Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",  # Replace with your Redis server and port
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

REDIS_HOST = "redis"
REDIS_PORT = 6379

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Accra"

USE_I18N = True

USE_TZ = True

SITE_ID = 1


ADMIN_URL = "secret_admin/"

# setting default admin for the website
ADMINS = [
    (
        """TeamKweku""",
        "tutsdjango@gmail.com",
    )
]

# SETTING ADMIN AS DEFAULT MANAGER
MANAGERS = ADMINS


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/staticfiles/"

STATIC_ROOT = str(ROOT_DIR / "staticfiles")

STATICFILES_DIRS = []

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = str(ROOT_DIR / "mediafiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_URLS_REGEX = r"^/api/.*$"

AUTH_USER_MODEL = "users.User"

AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    "axes.backends.AxesStandaloneBackend",
    # Django ModelBackend is the default authentication backend.
    "django.contrib.auth.backends.ModelBackend",
]

# Number of login attempts allowed before a block
AXES_FAILURE_LIMIT = 5
AXES_LOCK_OUT_AT_FAILURE = True
AXES_COOLOFF_TIME = 5
AXES_LOCKOUT_PARAMETERS = ["ip_address", "username", "user_agent"]
AXES_LOCK_OUT_BY = "combo"

# CELERY settings
CELERY_BROKER_URL = env("CELERY_BROKER")
CELERY_RESULT_BACKEND = env("CELERY_BACKEND")
CELERY_TIMEZONE = "Africa/Accra"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

REST_FRAMEWORK = {
    # using the custom exception handler in common
    "EXCEPTION_HANDLER": "core_apps.common.exceptions.common_exception_handler",
    "NON_FIELD_ERRORS_KEY": "error",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # enabling api rate-limiting
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",  # 100 requests per day for anonymous users
        "user": "1000/day",  # 1000 requests per day for authenticated users
    },
}


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": (
        "Bearer",
        "JWT",
    ),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=720),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SIGNING_KEY": env("SIGNING_KEY"),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "USERNAME_CHANGED_EMAIL_CONFIMATION": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "USERNAME_RESET_CONFIRM_URL": "email/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SERIALIZERS": {
        "user_create": "core_apps.users.serializers.CreateUserSerializer",
        "user": "core_apps.users.serializers.UserSerializer",
        "current_user": "core_apps.users.serializers.UserSerializer",
        "user_delete": "djoser.serializers.UserDeleteSerializer",
    },
}

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": ROOT_DIR / "whoosh_index",
    }
}
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

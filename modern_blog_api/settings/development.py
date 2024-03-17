# import setting from base and extending it in development
from .base import *  # noqa: F403
from .base import env

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-1a76b&-6t+*gpf21_66c2i#qp7rikjchit-rnidk=v2y!7ub88",
)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

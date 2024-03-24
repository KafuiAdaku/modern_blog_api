import os

from celery import Celery
from django.conf import settings

# change settings to .development or production based on the environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modern_blog_api.settings.development")

app = Celery("modern_blog_api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

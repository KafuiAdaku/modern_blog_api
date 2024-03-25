import os

from celery import Celery
from django.conf import settings

# change settings to .development or production based on the environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modern_blog_api.settings.production")

# Create Celery application
app = Celery("modern_blog_api")

# Load Celery configuration from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover tasks from all registered apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

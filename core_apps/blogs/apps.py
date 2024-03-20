from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogsConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "core_apps.blogs"
    verbose_name: str = _("Blogs")

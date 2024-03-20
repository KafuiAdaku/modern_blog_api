from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RatingsConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "core_apps.ratings"
    verbose_name: str = _("Ratings")

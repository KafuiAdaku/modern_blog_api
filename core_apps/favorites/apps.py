from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FavoritesConfig(AppConfig):
    """Config for the favorites app."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.favorites"
    verbose_name = _("Favorites")

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfilesConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "core_apps.profiles"
    verbose_name: str = _("Profiles")

    def ready(self) -> None:
        from core_apps.profiles import signals  # noqa: F401

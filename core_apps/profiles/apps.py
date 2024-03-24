from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfilesConfig(AppConfig):
    """
    Configuration class for the Profiles app.

    This class defines configuration options for
        the Profiles app.

    Attributes:
    - default_auto_field (str): Default primary key field
        type for models in this app.
    - name (str): Name of the app.
    - verbose_name (str): Verbose name of the app, used
        in the admin interface.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "core_apps.profiles"
    verbose_name: str = _("Profiles")

    def ready(self) -> None:
        from core_apps.profiles import signals  # noqa: F401

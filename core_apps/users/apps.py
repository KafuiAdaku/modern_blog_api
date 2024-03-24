from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """
    Configuration class for the Users app.

    This class defines configuration options for the Users app.

    Attributes:
    - default_auto_field (str): Default primary key field type
        for models in this app.
    - name (str): Name of the app.
    - verbose_name (str): Verbose name of the app, used
        in the admin interface.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "core_apps.users"
    verbose_name: str = _("Users")

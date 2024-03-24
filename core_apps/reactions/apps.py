from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ReactionsConfig(AppConfig):
    """
    Configuration class for the 'reactions' app.

    This class defines configuration options for the
        'reactions' app.

    Attributes:
    - default_auto_field (str): Specifies the name of the
        auto-created primary key field.
    - name (str): Specifies the name of the app.
    - verbose_name (str): Human-readable name for the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.reactions"
    verbose_name = _("Reactions")

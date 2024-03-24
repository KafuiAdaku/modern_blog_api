from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RatingsConfig(AppConfig):
    """
    Configuration class for the 'ratings' app.

    This class defines configuration options for the
        'ratings' app.

    Attributes:
    - default_auto_field (str): Specifies the name of
        the auto-created primary key field.
    - name (str): Specifies the name of the app.
    - verbose_name (str): Human-readable name for the app.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "core_apps.ratings"
    verbose_name: str = _("Ratings")

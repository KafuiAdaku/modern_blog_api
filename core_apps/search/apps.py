from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SearchConfig(AppConfig):
    """
    AppConfig class for the 'search' app.

    This class defines configuration options for the 'search' app.

    Attributes:
    - default_auto_field (str): Specifies the name of the
        auto-created primary key field.
    - name (str): Specifies the name of the app.
    - verbose_name (str): Human-readable name for the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.search"
    verbose_name = _("Search")

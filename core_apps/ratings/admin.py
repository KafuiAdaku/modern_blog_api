from typing import List

from django.contrib import admin

from .models import Rating


class RatingAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Rating model.

    This class defines the configuration options for
        the Rating model
    in the Django admin interface.

    Attributes:
    - list_display (list): The list of fields to
        display in the admin interface.
    """

    list_display: List[str] = ["blog", "rated_by", "value"]


admin.site.register(Rating, RatingAdmin)

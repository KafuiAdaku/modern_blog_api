from typing import List
from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for the Profile model.

    This class defines the administration interface for the Profile model.

    Attributes:
    - list_display (list[str]): Fields displayed in
        the list view of profiles.
    - list_filter (list[str]): Fields used for filtering
        profiles in the admin interface.
    - list_display_links (list[str]): Fields used
        for linking to the change page from the list view.
    """

    list_display: List[str] = ["pkid", "id", "user", "gender", "city"]
    list_filter: List[str] = ["gender", "city"]
    list_display_links: List[str] = ["id", "pkid"]


# Register the Profile model with the custom admin interface
admin.site.register(Profile, ProfileAdmin)

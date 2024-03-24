from typing import List

from django.contrib import admin

from . import models


class BlogAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Blog model.

    This class defines the admin interface for managing
        Blog objects.

    Attributes:
    - list_display (list): List of fields to display
        in the admin list view.
    - list_display_links (list): List of fields to use
        as links in the admin list view.
    """

    list_display: List[str] = ["pkid", "author", "slug", "blog_read_time", "views"]
    list_display_links: List[str] = ["pkid", "author"]


admin.site.register(models.Blog, BlogAdmin)

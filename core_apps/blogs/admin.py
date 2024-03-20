from django.contrib import admin
from typing import List
from . import models


class BlogAdmin(admin.ModelAdmin):
    """Blog Admin"""

    list_display: List[str] = ["pkid", "author", "slug", "blog_read_time", "views"]
    list_display_links: List[str] = ["pkid", "author"]


admin.site.register(models.Blog, BlogAdmin)

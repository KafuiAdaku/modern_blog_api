from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display: list[str] = ["pkid", "id", "user", "gender", "city"]
    list_filter: list[str] = ["gender", "city"]
    list_display_links: list[str] = ["id", "pkid"]


admin.site.register(Profile, ProfileAdmin)

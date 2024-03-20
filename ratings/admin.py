from django.contrib import admin
from typing import List
from .models import Rating


class RatingAdmin(admin.ModelAdmin):
    list_display: List[str] = ["blog", "rated_by", "value"]


admin.site.register(Rating, RatingAdmin)

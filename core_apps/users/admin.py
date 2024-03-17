from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from typing import List, Tuple, Any

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering: List[str] = ["email"]
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display: List[str] = [
        "pkid",
        "id",
        "email",
        "username",
        "is_staff",
        "is_active",
    ]
    list_display_links: List[str] = ["id", "email"]
    list_filter: List[str] = ["email", "username", "is_staff"]
    fieldsets: Tuple[Tuple[str, Any], ...] = (
        (
            _("Login Credentials"),
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Personal Information"),
            {"fields": ("username", "first_name", "last_name")},
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets: Tuple[Tuple[str, Any], ...] = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields: List[str] = ["email", "username", "first_name", "last_name"]


admin.site.register(User, UserAdmin)

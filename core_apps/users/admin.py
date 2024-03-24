from typing import Any, List, Tuple

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    """
    Custom User admin interface.

    This class defines the administration interface for the User model.

    Attributes:
    - ordering (List[str]): Field used for ordering the users list
        in the admin interface.
    - add_form: Form used for adding new users.
    - form: Form used for editing existing users.
    - model: User model managed by this admin interface.
    - list_display (List[str]): Fields displayed in the users list.
    - list_display_links (List[str]): Fields used for linking to
        the change page from the users list.
    - list_filter (List[str]): Fields used for filtering users
        in the admin interface.
    - fieldsets (Tuple[Tuple[str, Any], ...]): Fieldsets displayed
        in the user change form.
    - add_fieldsets (Tuple[Tuple[str, Any], ...]): Fieldsets displayed in
        the user add form.
    - search_fields (List[str]): Fields used for searching users in the
        admin interface.
    """

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


# Register the User model with the custom admin interface
admin.site.register(User, UserAdmin)

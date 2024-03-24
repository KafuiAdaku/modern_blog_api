from typing import Dict

from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Get the user model
User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    """
    Form for changing user information.

    This form is used in the Django admin interface for
        changing user information.

    Inherits from `admin_forms.UserChangeForm`.

    Attributes:
    - Meta (class): Inner class defining metadata
        options for the form.
    """

    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    """
    Form for creating a new user.

    This form is used in the Django admin interface for
        creating new users.

    Inherits from `admin_forms.UserCreationForm`.

    Attributes:
    - Meta (class): Inner class defining metadata options
        for the form.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        error_messages: Dict[str, Dict[str, str]] = {
            "username": {"unique": _("Username already exits!!.")}
        }

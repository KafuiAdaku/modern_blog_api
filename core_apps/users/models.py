import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing a user account.

    This model replaces the default Django User model with a custom one.

    Attributes:
    - pkid: Primary key for the user model.
    - id: Unique identifier for the user.
    - username: User's username.
    - first_name: User's first name.
    - last_name: User's last name.
    - email: User's email address.
    - is_staff: Indicates if the user is a staff member.
    - is_active: Indicates if the user account is active.
    - date_joined: Date and time when the user joined.
    - USERNAME_FIELD: Field used for authentication (email).
    - REQUIRED_FIELDS: List of fields required for creating a user (username).
    - objects: Custom manager for the user model.

    Methods:
    - __str__: Returns the username as a string.
    - get_full_name: Returns the full name of the user.
    """

    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(
        verbose_name=_("username"), db_index=True, max_length=255, unique=True
    )
    first_name = models.CharField(verbose_name=_("first name"), max_length=50)
    last_name = models.CharField(verbose_name=_("last name"), max_length=50)
    email = models.EmailField(
        verbose_name=_("email address"), db_index=True, unique=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list[str] = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name: str = _("user")
        verbose_name_plural: str = _("users")

    def __str__(self) -> str:
        return self.username

    @property
    def get_full_name(self) -> str:
        return f"{self.first_name.title()} {self.last_name.title()}"

import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
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
    REQUIRED_FIELDS: list[str] = ["username"]

    objects = CustomUserManager()

    class Meta:
        verbose_name: str = _("user")
        verbose_name_plural: str = _("users")

    def __str__(self) -> str:
        return self.username

    @property
    def get_full_name(self) -> str:
        return f"{self.first_name.title()} {self.last_name.title()}"

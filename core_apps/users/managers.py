from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model.

    This manager provides methods for creating and
        managing user accounts.

    Methods:
    - email_validator: Validate the email address format.
    - create_user: Create a new user account.
    - create_superuser: Create a new superuser account.
    """

    def email_validator(self, email: str) -> None:
        """
        Validate the format of the email address.

        Raises:
        - ValueError: If the email address is invalid.
        """

        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address"))

    def create_user(self, username: str, email: str, password: str, **extra_fields):
        """
        Create a new user account.

        Args:
        - username (str): User's username.
        - email (str): User's email address.
        - password (str): User's password.
        - extra_fields (dict): Extra fields for the user.

        Returns:
        - User: The created user object.

        Raises:
        - ValueError: If required fields are not provided or if
            the email address is invalid.
        """

        if not username:
            raise ValueError(_("Users must submit a username"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Base User Account: An email address is required"))

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username: str, email: str, password: str, **extra_fields
    ):
        """
        Create a new superuser account.

        Args:
        - username (str): User's username.
        - email (str): User's email address.
        - password (str): User's password.
        - extra_fields (dict): Extra fields for the user.

        Returns:
        - User: The created superuser object.

        Raises:
        - ValueError: If required fields are not provided, if the email
            address is invalid,or if the provided superuser flags are
            not set to True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superusers must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superusers must have is_superuser=True"))
        if not password:
            raise ValueError(_("Superusers must have a password"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Admin Account: An email address is required"))

        user = self.create_user(username, email, password, **extra_fields)
        user.save(using=self._db)
        return user

from typing import List

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.common.models import TimeStampedUUIDModel

# Get the user model
User = get_user_model()


class Profile(TimeStampedUUIDModel):
    """
    Model representing a user's profile.

    Attributes:
    - user (ForeignKey): One-to-one relationship with the User model.
    - about_me (TextField): Text field for the user's about me section.
    - gender (CharField): Field for the user's gender.
    - city (CharField): Field for the user's city.
    - profile_photo (ImageField): Field for the user's profile photo.
    - twitter_handle (CharField): Field for the user's Twitter handle.
    - facebook_account (CharField): Field for the user's Facebook account.
    - github_account (CharField): Field for the user's GitHub account.
    - follows (ManyToManyField): Many-to-many relationship with
        other profiles for following.
    """

    # Choices for gender field
    class Gender(models.TextChoices):
        MALE = "male", _("male")
        FEMALE = "female", _("female")
        OTHER = "other", _("other")

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)

    about_me: models.TextField = models.TextField(
        verbose_name=_("about me"),
        default="",
    )
    gender = models.CharField(
        verbose_name=_("gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )

    city: models.CharField = models.CharField(
        verbose_name=_("city"),
        max_length=180,
        default="Accra",
        blank=False,
        null=False,
    )
    profile_photo = models.ImageField(verbose_name=_("profile photo"), blank=True)
    twitter_handle = models.CharField(
        verbose_name=_("twitter_handle"), max_length=50, blank=True
    )
    facebook_account = models.CharField(
        verbose_name=_("facebook_account"), max_length=50, blank=True
    )
    github_account = models.CharField(
        verbose_name=_("github_account"), max_length=50, blank=True
    )
    follows = models.ManyToManyField(
        "self", symmetrical=False, related_name="followed_by", blank=True
    )

    def __str__(self) -> str:
        """
        Method to return a string representation of the profile.

        Returns:
        - str: String representation of the profile.
        """
        return f"{self.user.username}'s profile"

    # Implementing following and unfollowing feature
    def following_list(self) -> List["Profile"]:
        """
        Method to get the list of profiles that this profile is following.

        Returns:
        - List[Profile]: List of profiles that this profile is following.
        """
        return list(self.follows.all())

    def followers_list(self) -> List["Profile"]:
        """
        Method to get the list of profiles that are following this profile.

        Returns:
        - List[Profile]: List of profiles that are following this profile.
        """
        return list(self.followed_by.all())

    def follow(self, profile: "Profile") -> None:
        """
        Method to follow another profile.

        Args:
        - profile (Profile): Profile to follow.
        """
        self.follows.add(profile)

    def unfollow(self, profile: "Profile") -> None:
        """
        Method to unfollow a profile.

        Args:
        - profile (Profile): Profile to unfollow.
        """
        self.follows.remove(profile)

    def check_following(self, profile: "Profile") -> bool:
        """
        Method to check if this profile is following another profile.

        Args:
        - profile (Profile): Profile to check if following.

        Returns:
        - bool: True if following, False otherwise.
        """
        return self.follows.filter(pkid=profile.pkid).exists()

    def check_is_followed_by(self, profile: "Profile") -> bool:
        """
        Method to check if this profile is followed by another profile.

        Args:
        - profile (Profile): Profile to check if following.

        Returns:
        - bool: True if followed by, False otherwise.
        """
        return self.followed_by.filter(pkid=profile.pkid).exists()

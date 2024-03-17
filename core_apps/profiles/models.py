from typing import List

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Profile(TimeStampedUUIDModel):
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
    profile_photo = models.ImageField(
        verbose_name=_("profile photo"), default="/profile_default.png"
    )
    twitter_handle = models.CharField(
        verbose_name=_("twitter_handle"), max_length=20, blank=True
    )
    facebook_account = models.CharField(
        verbose_name=_("facebook_account"), max_length=20, blank=True
    )
    github_account = models.CharField(
        verbose_name=_("twitter_account"), max_length=20, blank=True
    )
    follows = models.ManyToManyField(
        "self", symmetrical=False, related_name="followed_by", blank=True
    )

    def __str__(self) -> str:
        return f"{self.user.username}'s profile"

    # Implementing following and unfollowing feature
    def following_list(self) -> List['Profile']:
        return list(self.follows.all())

    def followers_list(self) -> List['Profile']:
        return list(self.followed_by.all())

    def follow(self, profile: 'Profile') -> None:
        self.follows.add(profile)

    def unfollow(self, profile: 'Profile') -> None:
        self.follows.remove(profile)

    def check_following(self, profile: 'Profile') -> bool:
        return self.follows.filter(pkid=profile.pkid).exists()

    def check_is_followed_by(self, profile: 'Profile') -> bool:
        return self.followed_by.filter(pkid=profile.pkid).exists()

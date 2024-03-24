from typing import Any, List

from django.conf import settings
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model.

    This class defines the serialization behavior for the Profile model.

    Attributes:
    - username (str): Username of the user associated with the profile.
    - first_name (str): First name of the user associated with the profile.
    - last_name (str): Last name of the user associated with the profile.
    - email (str): Email address of the user associated with the profile.
    - full_name (str): Full name of the user associated with the profile.
    - profile_photo (str): URL of the profile photo.
    - following (bool): Indicates if the requesting user is following
        the profile owner.
    """

    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    profile_photo = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields: List[str] = [
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "id",
            "profile_photo",
            "about_me",
            "gender",
            "city",
            "twitter_handle",
            "facebook_account",
            "github_account",
            "following",
        ]

    def get_full_name(self, obj: Profile) -> str:
        """
        Returns the full name of the user associated with
            the profile.

        Args:
        - obj (Profile): Profile instance.

        Returns:
        - str: Full name of the user.
        """
        first_name: str = obj.user.first_name.title()
        last_name: str = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def get_profile_photo(self, obj: Profile) -> str:
        """
        Returns the URL of the profile photo.

        Args:
        - obj (Profile): Profile instance.

        Returns:
        - str: URL of the profile photo.
        """
        if obj.profile_photo and obj.profile_photo.name.startswith(settings.MEDIA_URL):
            request = self.context.get("request")
            if request is not None:
                return request.build_absolute_uri(obj.profile_photo.url)
            else:
                return obj.profile_photo.url
        else:
            # If the profile_photo is a URL, return it as-is
            return obj.profile_photo.name

    def get_following(self, instance: Profile) -> bool:
        """
        Returns whether the requesting user is following the
            profile owner.

        Args:
        - instance (Profile): Profile instance.

        Returns:
        - bool: Indicates if the requesting user is following
            the profile owner.
        """
        request: Any = self.context.get("request", None)
        if request is None:
            return None
        if request.user.is_anonymous:
            return False

        current_user_profile: Profile = request.user.profile
        followee: Profile = instance
        following_status: bool = current_user_profile.check_following(followee)
        return following_status


class UpdateProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Profile model.

    This class defines the serialization behavior for
        updating Profile model.

    Attributes:
    - profile_photo (str): URL of the profile photo.
    - about_me (str): About me information.
    - gender (str): Gender of the user.
    - city (str): City of the user.
    - twitter_handle (str): Twitter handle of the user.
    - facebook_account (str): Facebook account of the user.
    - github_account (str): GitHub account of the user.
    """

    class Meta:
        model = Profile
        fields: List[str] = [
            "profile_photo",
            "about_me",
            "gender",
            "city",
            "twitter_handle",
            "facebook_account",
            "github_account",
        ]


class FollowingSerializer(serializers.ModelSerializer):
    """
    Serializer for following profile list.

    This class defines the serialization behavior for following
        profile list.

    Attributes:
    - username (str): Username of the user.
    - first_name (str): First name of the user.
    - last_name (str): Last name of the user.
    - profile_photo (str): URL of the profile photo.
    - about_me (str): About me information.
    - twitter_handle (str): Twitter handle of the user.
    - following (bool): Indicates if the user is following the profile.
    - facebook_account (str): Facebook account of the user.
    - github_account (str): GitHub account of the user.
    """

    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    following = serializers.BooleanField(default=True)

    class Meta:
        model = Profile
        fields: List[str] = [
            "username",
            "first_name",
            "last_name",
            "profile_photo",
            "about_me",
            "twitter_handle",
            "following",
            "facebook_account",
            "github_account",
        ]

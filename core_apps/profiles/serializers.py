from rest_framework import serializers
from typing import Any, List

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
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
        first_name: str = obj.user.first_name.title()
        last_name: str = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def get_profile_photo(self, obj: Profile) -> str:
        return obj.profile_photo.url

    def get_following(self, instance: Profile) -> bool:
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

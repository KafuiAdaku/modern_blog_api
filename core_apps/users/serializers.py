from typing import Any, Dict

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

# Get the user model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user model.

    This serializer is used for representing user data in the API responses.

    Attributes:
    - gender (serializers.CharField): Field representing the user's gender.
    - profile_photo (serializers.ReadOnlyField): Field representing the
        user's profile photo.
    - city (serializers.CharField): Field representing the user's city.
    - first_name (serializers.SerializerMethodField): Field representing
        the user's first name.
    - last_name (serializers.SerializerMethodField): Field representing
        the user's last name.

    Methods:
    - get_first_name: Get the formatted first name.
    - get_last_name: Get the formatted last name.
    - to_representation: Custom representation for the serializer.
    """

    gender = serializers.CharField(source="profile.gender")
    profile_photo = serializers.ReadOnlyField(source="profile.profile_photo")
    city = serializers.CharField(source="profile.city")
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "gender",
            "profile_photo",
            "city",
        ]

    def get_first_name(self, obj: Any) -> str:
        return obj.first_name.title()

    def get_last_name(self, obj: Any) -> str:
        return obj.last_name.title()

    def get_full_name(self, obj: Any):
        """Get the formatted first name."""
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def to_representation(self, instance: Any) -> Dict[str, Any]:
        """Custom representation for the serializer."""
        representation = super(UserSerializer, self).to_representation(instance)
        # Add 'admin' field if user is a superuse
        if instance.is_superuser:
            representation["admin"] = True
        return representation


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password"]

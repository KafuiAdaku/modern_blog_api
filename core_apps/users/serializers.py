from typing import Any, Dict

from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
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
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def to_representation(self, instance: Any) -> Dict[str, Any]:
        representation = super(UserSerializer, self).to_representation(instance)
        if instance.is_superuser:
            representation["admin"] = True
        return representation


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password"]

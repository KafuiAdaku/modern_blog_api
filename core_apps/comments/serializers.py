from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Comment

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer."""
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj) -> str:
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj: Comment) -> str:
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    class Meta:
        """Meta class."""
        model = Comment
        fields = ["id", "author",
                  "article", "body", "created_at", "updated_at"]


class CommentListSerializer(serializers.ModelSerializer):
    """Comment list serializer."""
    author = serializers.ReadOnlyField(source="author.user.username")
    article = serializers.ReadOnlyField(source="blog.title")
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj: Comment) -> str:
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj: Comment) -> str:
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    class Meta:
        """Meta class."""
        model = Comment
        fields = ["id", "author", "blog", "body", "created_at", "updated_at"]

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Comment

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for individual comments.

    This serializer serializes individual comment objects.

    Attributes:
    - created_at (SerializerMethodField): Method field
        to serialize creation date.
    - updated_at (SerializerMethodField): Method field
        to serialize last update date.
    """

    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj) -> str:
        """
        Get the creation date of the comment.

        Args:
        - obj: The comment object.

        Returns:
        - str: The formatted creation date string.
        """
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj: Comment) -> str:
        """
        Get the last update date of the comment.

        Args:
        - obj (Comment): The comment object.

        Returns:
        - str: The formatted last update date string.
        """
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    class Meta:
        """
        Meta class for CommentSerializer.

        Attributes:
        - model (Comment): The Comment model to serialize.
        - fields (list): The fields to include in the serialization.
        """

        model = Comment
        fields = ["id", "author", "blog", "body", "created_at", "updated_at"]


class CommentListSerializer(serializers.ModelSerializer):
    """
    Serializer for lists of comments.

    This serializer serializes lists of comment objects.

    Attributes:
    - author (ReadOnlyField): Read-only field to serialize
        comment author's username.
    - blog (ReadOnlyField): Read-only field to serialize
        blog title.
    - created_at (SerializerMethodField): Method field to
        serialize creation date.
    - updated_at (SerializerMethodField): Method field to
        serialize last update date.
    """

    author = serializers.ReadOnlyField(source="author.user.username")
    blog = serializers.ReadOnlyField(source="blog.title")
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj: Comment) -> str:
        """
        Get the creation date of the comment.

        Args:
        - obj (Comment): The comment object.

        Returns:
        - str: The formatted creation date string.
        """
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj: Comment) -> str:
        """
        Get the last update date of the comment.

        Args:
        - obj (Comment): The comment object.

        Returns:
        - str: The formatted last update date string.
        """
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    class Meta:
        """
        Meta class for CommentListSerializer.

        Attributes:
        - model (Comment): The Comment model to serialize.
        - fields (list): The fields to include in the serialization.
        """

        model = Comment
        fields = ["id", "author", "blog", "body", "created_at", "updated_at"]

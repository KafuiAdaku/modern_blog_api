from rest_framework import serializers

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rating model.

    This serializer serializes instances of the Rating model.

    Attributes:
    - rated_by (str): Serializer method field to represent
        the user who rated the blog.
    - blog (str): Serializer method field to represent
        the title of the rated blog.
    - Meta (class): Inner class defining metadata options
        for the serializer.
    """

    rated_by: str = serializers.SerializerMethodField(read_only=True)
    blog: str = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """
        Meta class for the RatingSerializer.

        Attributes:
        - model (Rating): The model to serialize.
        - fields (list): The fields to include in
            the serialization.
        """

        model = Rating
        fields = ["id", "blog", "rated_by", "value"]

    def get_rated_by(self, obj: Rating) -> str:
        """
        Get the username of the user who rated the blog.

        Args:
        - obj (Rating): The Rating object.

        Returns:
        - str: The username of the user who rated the blog.
        """
        return obj.rated_by.username

    def get_blog(self, obj: Rating) -> str:
        """
        Get the title of the rated blog.

        Args:
        - obj (Rating): The Rating object.

        Returns:
        - str: The title of the rated blog.
        """
        return obj.blog.title

from rest_framework import serializers

from .models import Reaction


class ReactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Reaction model.

    This serializer serializes instances of the
        Reaction model.

    Attributes:
    - created_at (str): Serializer method field to
        represent the creation date.
    - Meta (class): Inner class defining metadata
        options for the serializer.
    """

    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj: Reaction) -> str:
        """
        Get the formatted creation date of the reaction.

        Args:
        - obj (Reaction): The Reaction object.

        Returns:
        - str: The formatted creation date.
        """
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    class Meta:
        """
        Meta options for the ReactionSerializer.

        Attributes:
        - model (Reaction): The model to serialize.
        - exclude (list): The fields to exclude
            from the serialization.
        """

        model = Reaction
        exclude = ["pkid", "updated_at"]

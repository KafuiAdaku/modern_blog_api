from rest_framework import serializers

from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Favorite model.

    This serializer serializes instances of the Favorite model.

    Attributes:
    - Meta (class): Inner class defining metadata options for the serializer.
    """

    class Meta:
        """
        Meta class for the FavoriteSerializer.

        Attributes:
        - model (Favorite): The model to serialize.
        - fields (list): The fields to include in the serialization.
        """

        model = Favorite
        fields = ["id", "user", "blog"]

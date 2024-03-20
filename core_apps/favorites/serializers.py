from rest_framework import serializers

from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for the Favorite model."""
    class Meta:
        """Meta class for the FavoriteSerializer."""
        model = Favorite
        fields = ["id", "user", "blog"]

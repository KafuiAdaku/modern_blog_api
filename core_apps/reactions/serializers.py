from rest_framework import serializers

from .models import Reaction


class ReactionSerializer(serializers.ModelSerializer):
    """Serializer for Reaction model."""
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj: Reaction) -> str:
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    class Meta:
        """Meta options."""
        model = Reaction
        exclude = ["pkid", "updated_at"]

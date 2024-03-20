from rest_framework import serializers

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    rated_by: str = serializers.SerializerMethodField(read_only=True)
    blog: str = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "article", "rated_by", "value"]

    def get_rated_by(self, obj: Rating) -> str:
        return obj.rated_by.username

    def get_blog(self, obj: Rating) -> str:
        return obj.blog.title

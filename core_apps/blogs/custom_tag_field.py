from rest_framework import serializers
from django.db.models import QuerySet
from .models import Tag


class TagRelatedField(serializers.RelatedField):
    """Custom Tag Related Field"""
    def get_queryset(self) -> QuerySet[Tag]:
        """Get Queryset"""
        return Tag.objects.all()

    def to_internal_value(self, data) -> Tag:
        """To Internal Value"""
        tag, created = Tag.objects.get_or_create(tag=data, slug=data.lower())

        return tag

    def to_representation(self, value) -> str:
        """To Representation"""
        return value.tag
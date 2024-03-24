from rest_framework import serializers
from django.db.models import QuerySet
from .models import Tag


class TagRelatedField(serializers.RelatedField):
    """
    Custom related field for Tag model.

    This field is used to represent and validate relationships
        with Tag model.

    Methods:
    - get_queryset(): Get the queryset for Tag objects.
    - to_internal_value(data): Convert external data to
        internal Tag object.
    - to_representation(value): Convert Tag object
        to string representation.
    """

    def get_queryset(self) -> QuerySet[Tag]:
        """Get the queryset for Tag objects."""
        return Tag.objects.all()

    def to_internal_value(self, data) -> Tag:
        """Convert external data to internal Tag object."""
        tag, created = Tag.objects.get_or_create(tag=data, slug=data.lower())

        return tag

    def to_representation(self, value) -> str:
        """Convert Tag object to string representation."""
        return value.tag

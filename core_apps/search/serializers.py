from drf_haystack.serializers import HaystackSerializer

from core_apps.search.search_indexes import BlogIndex


class BlogSearchSerializer(HaystackSerializer):
    """BlogSearchSerializer class."""

    class Meta:
        """Meta class."""

        index_classes = [BlogIndex]

        fields = ["author", "title", "body", "autocomplete", "created_at", "updated_at"]
        ignore_fields = ["autocomplete"]
        field_aliases = {"q": "autocomplete"}

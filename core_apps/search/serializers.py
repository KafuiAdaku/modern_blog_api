from drf_haystack.serializers import HaystackSerializer

from core_apps.search.search_indexes import BlogIndex


class BlogSearchSerializer(HaystackSerializer):
    """
    Serializer for searching blog articles.

    This serializer is used to search for blog
        articles using Haystack.

    Attributes:
    - Meta (class): Inner class defining metadata
        options for the serializer.
    """

    class Meta:
        """
        Meta options for the BlogSearchSerializer.

        Attributes:
        - index_classes (list): List of search indexes to use.
        - fields (list): List of fields to include in the
            search results.
        - ignore_fields (list): List of fields to ignore in
            the search results.
        - field_aliases (dict): Mapping of field aliases for
            search queries.
        """

        index_classes = [BlogIndex]

        fields = ["author", "title", "body", "autocomplete", "created_at", "updated_at"]
        ignore_fields = ["autocomplete"]
        field_aliases = {"q": "autocomplete"}

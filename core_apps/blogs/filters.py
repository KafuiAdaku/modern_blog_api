import django_filters as filters
from django.db.models import QuerySet

from core_apps.blogs.models import Blog


class BlogFilter(filters.FilterSet):
    """
    Filter set for filtering blog articles.

    This filter set provides filters for querying blog
        articles based on various criteria.

    Attributes:
    - author: Filter for filtering by author's first name.
    - title: Filter for filtering by title.
    - tags: Filter for filtering by tags associated with the blog.
    - created_at: Filter for filtering by creation date.
    - updated_at: Filter for filtering by last update date.
    """

    author = filters.CharFilter(
        field_name="author__first_name", lookup_expr="icontains"
    )
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    tags = filters.CharFilter(
        field_name="tags", method="get_blog_tags", lookup_expr="iexact"
    )
    created_at = filters.IsoDateTimeFilter(field_name="created_at")
    updated_at = filters.IsoDateTimeFilter(field_name="updated_at")

    class Meta:
        """Meta class for BlogFilter."""

        model = Blog
        fields = ["author", "title", "tags", "created_at", "updated_at"]

    def get_blog_tags(self, queryset: QuerySet, tags: str, value: str) -> QuerySet:
        """
        Custom method to filter blogs by tags.

        Args:
        - queryset (QuerySet): The queryset to filter.
        - tags (str): Name of the tags field.
        - value (str): Value to filter by.

        Returns:
        - QuerySet: Filtered queryset.
        """
        tag_values = value.replace(" ", "").split(",")
        return queryset.filter(tags__tag__in=tag_values).distinct()

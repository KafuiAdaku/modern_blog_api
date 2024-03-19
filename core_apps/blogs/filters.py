import django_filters as filters
from django.db.models import QuerySet
from core_apps.articles.models import Article


class Filter(filters.FilterSet):
    """Blog Filter"""
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
        """Meta"""
        model = Blog
        fields = ["author", "title", "tags", "created_at", "updated_at"]

    def get_blog_tags(self, queryset: QuerySet, tags: str, value: str) \
            -> QuerySet:
        tag_values = value.replace(" ", "").split(",")
        return queryset.filter(tags__tag__in=tag_values).distinct()

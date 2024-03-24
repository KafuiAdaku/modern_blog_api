from drf_haystack import viewsets
from drf_haystack.filters import HaystackAutocompleteFilter
from rest_framework import permissions

from core_apps.blogs.models import Blog

from .serializers import BlogSearchSerializer


class SearchBlogView(viewsets.HaystackViewSet):
    """
    View for searching blog articles.

    This view provides endpoints for searching blog articles
        using Haystack.

    Attributes:
    - permission_classes (list): List of permission classes
        for the view.
    - index_models (list): List of index models to search.
    - serializer_class (BlogSearchSerializer): Serializer
        class for the view.
    - filter_backends (list): List of filter backends
        for the view.
    """

    permission_classes = [permissions.AllowAny]
    index_models = [Blog]
    serializer_class = BlogSearchSerializer
    filter_backends = [HaystackAutocompleteFilter]

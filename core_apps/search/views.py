from drf_haystack import viewsets
from drf_haystack.filters import HaystackAutocompleteFilter
from rest_framework import permissions

from core_apps.blogs.models import Blog

from .serializers import BlogSearchSerializer


class SearchBlogView(viewsets.HaystackViewSet):
    """Views for blog search"""

    permission_classes = [permissions.AllowAny]
    index_models = [Blog]
    serializer_class = BlogSearchSerializer
    filter_backends = [HaystackAutocompleteFilter]

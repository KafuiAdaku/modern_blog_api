import logging
from typing import Dict, List

import redis
from django.conf import settings
from django.contrib.auth import get_user_model

# Redis cache imports
from django.core.cache import cache
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from core_apps.blogs.models import Blog, BlogViews

from .exceptions import UpdateBlog
from .filters import BlogFilter
from .pagination import BlogPagination
from .permissions import IsOwnerOrReadOnly
from .renderers import BlogJSONRenderer, BlogsJSONRenderer
from .serializers import BlogCreateSerializer, BlogSerializer, BlogUpdateSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


class BlogListAPIView(generics.ListAPIView):
    """
    List all blogs.

    Attributes:
    - serializer_class: The serializer class for blogs.
    - permission_classes: The permission classes for accessing this view.
    - queryset: The queryset containing all blogs.
    - renderer_classes: The renderer classes for rendering the response.
    - pagination_class: The pagination class for paginating the results.
    - filter_backends: The filter backends used for filtering the queryset.
    - filterset_class: The filter set class used for filtering.
    - ordering_fields: The fields available for ordering the queryset.
    """

    serializer_class = BlogSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Blog.objects.all()
    renderer_classes = (BlogsJSONRenderer,)
    pagination_class = BlogPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BlogFilter
    ordering_fields = ["created_at", "username"]

    # Redis cache configuration
    redis_instance = redis.StrictRedis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
    )

    @method_decorator(cache_page(60 * 60 * 2))  # Cache for 2 hours
    def dispatch(self, *args, **kwargs):
        return super(BlogListAPIView, self).dispatch(*args, **kwargs)


class BlogCreateAPIView(generics.CreateAPIView):
    """
    Create a blog.

    Attributes:
    - permission_classes: The permission classes for
        accessing this view.
    - serializer_class: The serializer class for creating a blog.
    - renderer_classes: The renderer classes for rendering
        the response.
    """

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = BlogCreateSerializer
    renderer_classes = [BlogJSONRenderer]

    def create(self, request: HttpRequest, *args: List, **kwargs: Dict) -> Response:
        """
        Create a blog.

        Args:
        - request (HttpRequest): The HTTP request.
        - args (List): Additional positional arguments.
        - kwargs (Dict): Additional keyword arguments.

        Returns:
        - Response: The HTTP response.
        """
        user = request.user
        data = request.data
        data["author"] = user.pkid
        serializer = self.serializer_class(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(
            f"blog {serializer.data.get('title')} \
            created by {user.username}"
        )

        # Clear the cache
        cache.delete("BlogListAPIView")

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BlogDetailView(APIView):
    """
    Get a blog.

    Attributes:
    - renderer_classes: The renderer classes for rendering the response.
    - permission_classes: The permission classes for accessing this view.
    """

    renderer_classes = [BlogJSONRenderer]
    permission_classes = [permissions.AllowAny]

    def get(self, request: HttpRequest, slug: str) -> Response:
        """
        Get a blog by slug.

        Args:
        - request (HttpRequest): The HTTP request.
        - slug (str): The slug of the blog.

        Returns:
        - Response: The HTTP response.
        """
        blog = Blog.objects.get(slug=slug)

        # Getting IP address of user to increase blogs view count
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        if not BlogViews.objects.filter(blog=blog, ip=ip).exists():
            BlogViews.objects.create(blog=blog, ip=ip)

            blog.views += 1
            blog.save()

        serializer = BlogSerializer(blog, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def update_blog_api_view(request: HttpRequest, slug: str) -> Response:
    """
    Update a blog.

    Args:
    - request (HttpRequest): The HTTP request.
    - slug (str): The slug of the blog to update.

    Returns:
    - Response: The HTTP response.
    """
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        raise NotFound("That blog does not exist in our catalog")

    user = request.user
    if blog.author != user:
        raise UpdateBlog

    if request.method == "PATCH":
        data = request.data
        serializer = BlogUpdateSerializer(blog, data=data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BlogDeleteAPIView(generics.DestroyAPIView):
    """
    Delete a blog.

    Attributes:
    - permission_classes: The permission classes for accessing this view.
    - queryset: The queryset containing all blogs.
    - lookup_field: The field to use for looking up the blog.
    """

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Blog.objects.all()
    lookup_field = "slug"

    def delete(self, request: HttpRequest, *args: List, **kwargs: Dict) -> Response:
        """
        Delete a blog.

        Args:
        - request (HttpRequest): The HTTP request.
        - args (List): Additional positional arguments.
        - kwargs (Dict): Additional keyword arguments.

        Returns:
        - Response: The HTTP response.
        """
        try:
            blog = Blog.objects.get(slug=self.kwargs.get("slug"))  # noqa: F841
        except Blog.DoesNotExist:
            raise NotFound("That blog does not exist in our catalog")

        delete_operation = self.destroy(request)
        data = {}
        if delete_operation:
            data["success"] = "Deletion was successful"

        else:
            data["failure"] = "Deletion failed"

        return Response(data=data)

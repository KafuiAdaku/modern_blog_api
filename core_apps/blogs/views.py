import logging
from typing import List, Dict
from django.http import HttpRequest

from django.contrib.auth import get_user_model
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
from .serializers import (
    BlogCreateSerializer,
    BlogSerializer,
    BlogUpdateSerializer,
)

User = get_user_model()

logger = logging.getLogger(__name__)


class BlogListAPIView(generics.ListAPIView):
    """List all blogs"""

    serializer_class = BlogSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Blog.objects.all()
    renderer_classes = (BlogsJSONRenderer,)
    pagination_class = BlogPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BlogFilter
    ordering_fields = ["created_at", "username"]


class BlogCreateAPIView(generics.CreateAPIView):
    """Create a blog"""

    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = BlogCreateSerializer
    renderer_classes = [BlogJSONRenderer]

    def create(self, request: HttpRequest, *args: List, **kwargs: Dict) -> Response:
        """Create a blog"""
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BlogDetailView(APIView):
    """Get a blog"""

    renderer_classes = [BlogJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest, slug: str) -> Response:
        """Get a blog by slug"""
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
    """Update a blog"""
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
    """Delete a blog"""

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Blog.objects.all()
    lookup_field = "slug"

    def delete(self, request: HttpRequest, *args: List, **kwargs: Dict) -> Response:
        """Delete a blog"""
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

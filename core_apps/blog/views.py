import logging

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from core_apps.articles.models import Blog, BlogViews

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

    def create(self, request: Request, *args: list,
               **kwargs: dict) -> Response:
        """Create a blog"""
        user = request.user
        data = request.data
        data["author"] = user.pkid
        serializer = self.serializer_class(data=data,
                                           context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(
            f"article {serializer.data.get('title')} \
            created by {user.username}"
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BlogDetailView(APIView):
    """Get a blog"""
    renderer_classes = [BlogJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, slug: str) -> Response:
        """Get a blog by slug"""
        article = Blog.objects.get(slug=slug)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        if not BlogViews.objects.filter(article=blog, ip=ip).exists():
            BlogViews.objects.create(article=blog, ip=ip)

            blog.views += 1
            blog.save()

        serializer = BlogSerializer(blog, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def update_article_api_view(request: Request, slug: str) -> Response:
    """Update a blog"""
    try:
        article = blog.objects.get(slug=slug)
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

    def delete(self, request: Request, *args: list,
               **kwargs: dict) -> Response:
        """Delete a blog"""
        try:
            blog = Blog.objects.get(slug=self.kwargs.get("slug"))
        except Blog.DoesNotExist:
            raise NotFound("That blog does not exist in our catalog")

        delete_operation = self.destroy(request)
        data = {}
        if delete_operation:
            data["success"] = "Deletion was successful"

        else:
            data["failure"] = "Deletion failed"

        return Response(data=data)

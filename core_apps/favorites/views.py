from rest_framework.request import Request
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core_apps.blogs.models import Blog
from core_apps.blogs.serializers import BlogCreateSerializer

from .exceptions import AlreadyFavorited
from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteAPIView(generics.CreateAPIView):
    """
    API view for favoriting a blog.

    This view allows authenticated users to favorite a blog.

    Permissions:
    - IsAuthenticated: Only authenticated users are
        allowed to access this view.

    Methods:
    - post: Create a favorite.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def post(self, request: Request, slug: str) -> Response:
        """
        Create a favorite.

        Args:
        - request (Request): The HTTP request object.
        - slug (str): The slug of the blog.

        Returns:
        - Response: HTTP response object.
        """
        data = request.data
        blog = Blog.objects.get(slug=slug)
        user = request.user

        favorite = Favorite.objects.filter(user=user, blog=blog.pkid).first()

        if favorite:
            raise AlreadyFavorited
        else:
            data["blog"] = blog.pkid
            data["user"] = user.pkid
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            data = serializer.data
            data["message"] = "Blog added to favorites."
            return Response(data, status=status.HTTP_201_CREATED)


class ListUserFavoriteBlogsAPIView(APIView):
    """
    API view for listing user favorite blogs.

    This view allows authenticated users to list their favorite blogs.

    Permissions:
    - IsAuthenticated: Only authenticated users are allowed to access this view.

    Methods:
    - get: List user favorite blogs.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        List user favorite blogs.

        Args:
        - request (Request): The HTTP request object.

        Returns:
        - Response: HTTP response object.
        """
        Favorites = Favorite.objects.filter(user_id=request.user.pkid)

        favorite_blogs = []
        for favorite in Favorites:
            blog = Blog.objects.get(pkid=favorite.blog.pkid)
            blog = BlogCreateSerializer(
                blog, context={"blog": blog.slug, "request": request}
            ).data
            favorite_blogs.append(blog)
        favorites = {"my_favorites": favorite_blogs}
        return Response(data=favorites, status=status.HTTP_200_OK)

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from core_apps.articles.models import Blog 
from core_apps.blogs.serializers import BlogCreateSerializer

from .exceptions import AlreadyFavorited
from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteAPIView(generics.CreateAPIView):
    """View for favoriting a blog."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    def post(self, request: Request, slug: str) -> Response:
        """Create a favorite."""
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
    """View for listing user favorite blogs."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        """List user favorite blogs."""
        Favorites = Favorite.objects.filter(user_id=request.user.pkid)

        favorite_articles = []
        for favorite in Favorites:
            article = Article.objects.get(pkid=favorite.article.pkid)
            article = ArticleCreateSerializer(
                article, context={"article": article.slug, "request": request}
            ).data
            favorite_articles.append(article)
        favorites = {"my_favorites": favorite_articles}
        return Response(data=favorites, status=status.HTTP_200_OK)

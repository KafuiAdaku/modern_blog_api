from django.http import Request
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import Any, List, Dict, Tuple

from core_apps.blogs.models import Blog

from .models import Reaction
from .serializers import ReactionSerializer


def find_blog_helper(slug: str) -> Blog:
    """Helper function to find an blog by slug."""
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        raise NotFound(f"Blog with the slug {slug} does not exist.")
    return blog


class ReactionAPIView(APIView):
    """API view for setting user reactions on articles."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReactionSerializer

    def set_reaction(self, blog: Blog, user: Any, reaction: Reaction) -> Tuple:
        """Set user reaction on an blog."""
        try:
            existing_reaction = Reaction.objects.get(blog=blog, user=user)
            existing_reaction.delete()
        except Reaction.DoesNotExist:
            pass

        data = {"blog": blog.pkid, "user": user.pkid, "reaction": reaction}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {"message": "Reaction successfully set"}
        status_code = status.HTTP_201_CREATED
        return response, status_code

    def post(self, request: Request, *args: List, **kwargs: Dict) -> Response:
        """Set user reaction on an blog."""
        slug = self.kwargs.get("slug")
        blog = find_blog_helper(slug)
        user = request.user
        reaction = request.data.get("reaction")

        try:
            existing_same_reaction = Reaction.objects.get(
                blog=blog, user=user, reaction=reaction
            )
            existing_same_reaction.delete()
            response = {
                "message": f"You no-longer \
                {'LIKE' if reaction in [1,'1'] else 'DISLIKE'}"
            }
            status_code = status.HTTP_200_OK
        except Reaction.DoesNotExist:
            response, status_code = self.set_reaction(blog, user, reaction)

        return Response(response, status_code)

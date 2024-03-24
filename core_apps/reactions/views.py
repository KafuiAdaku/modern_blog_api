from typing import Any, Dict, List, Tuple

from django.http import HttpRequest
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from core_apps.blogs.models import Blog

from .models import Reaction
from .serializers import ReactionSerializer


def find_blog_helper(slug: str) -> Blog:
    """
    Helper function to find a blog by slug.

    Args:
    - slug (str): The slug of the blog.

    Returns:
    - Blog: The blog object if found.

    Raises:
    - NotFound: If the blog with the specified slug does not exist.
    """
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        raise NotFound(f"Blog with the slug {slug} does not exist.")
    return blog


class ReactionAPIView(APIView):
    """
    API view for setting user reactions on articles.

    This view allows authenticated users to set
        reactions (like/dislike) on blog articles.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReactionSerializer

    def set_reaction(self, blog: Blog, user: Any, reaction: Reaction) -> Tuple:
        """
        Set user reaction on a blog.

        Args:
        - blog (Blog): The blog object.
        - user (Any): The user object.
        - reaction (Reaction): The reaction object.

        Returns:
        - Tuple: A tuple containing the response message
            and HTTP status code.
        """
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

    def post(self, request: HttpRequest, *args: List, **kwargs: Dict) -> Response:
        """
        Set user reaction on a blog.

        This method handles the POST request for setting
            user reactions on blog articles.

        Args:
        - request (HttpRequest): The HTTP request object.
        - *args (List): Variable-length argument list.
        - **kwargs (Dict): Keyword arguments.

        Returns:
        - Response: HTTP response object.
        """
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

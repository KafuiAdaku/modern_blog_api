from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from core_apps.blogs.models import Blog

from .exceptions import AlreadyRated, CantRateYourBlog
from .models import Rating


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_blog_rating_view(request, blog_id):
    """
    API view for creating a rating for a blog.

    This view allows authenticated users to rate a blog post.

    Permissions:
    - IsAuthenticated: Only authenticated users are allowed
        to access this view.

    Args:
    - request: The HTTP request object.
    - blog_id (int): The ID of the blog post.

    Returns:
    - Response: HTTP response object.
    """
    author = request.user
    blog = Blog.objects.get(id=blog_id)
    data = request.data

    if blog.author == author:
        raise CantRateYourBlog

    already_exists = blog.blog_ratings.filter(rated_by__pkid=author.pkid).exists()
    if already_exists:
        raise AlreadyRated
    elif data["value"] == 0:
        formatted_response = {"detail": "You can't give a zero rating"}
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)
    else:
        rating = Rating.objects.create(  # noqa: F841
            blog=blog,
            rated_by=request.user,
            value=data["value"],
            review=data["review"],
        )

        return Response(
            {"success": "Rating has been added"}, status=status.HTTP_201_CREATED
        )

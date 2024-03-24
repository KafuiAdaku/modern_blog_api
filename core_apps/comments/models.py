from django.contrib.auth import get_user_model
from django.db import models

from core_apps.common.models import TimeStampedUUIDModel

# Get User Model
User = get_user_model()


class Comment(TimeStampedUUIDModel):
    """
    Model representing comments on blogs.

    This model represents comments made on blog posts.

    Attributes:
    - blog (ForeignKey): The blog post to which the comment belongs.
    - author (ForeignKey): The user who authored the comment.
    - body (TextField): The content of the comment.
    """

    blog = models.ForeignKey(
        "blogs.Blog", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self) -> str:
        """
        Return a string representation of the comment.

        Returns:
        - str: A string representing the comment author and blog.
        """
        return f"{self.author} commented on {self.blog}"

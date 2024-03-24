from django.contrib.auth import get_user_model
from django.db import models

from core_apps.blogs.models import Blog
from core_apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Favorite(TimeStampedUUIDModel):
    """
    Model representing favorites.

    This model represents the relationship between
        users and their
    favorite blogs.

    Attributes:
    - user (ForeignKey): The user who favorited the blog.
    - blog (ForeignKey): The blog that is favorited.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="blog_favorites"
    )

    def __str__(self) -> str:
        """
        Return a string representation of the favorite.

        Returns:
        - str: A string representing the user and the favorited blog.
        """
        return f"{self.user.username} favorited {self.blog.title}"

    def is_favorited(self, user, blog: str) -> bool:
        """
        Check if a blog is favorited by a user.

        Args:
        - user: The user.
        - blog (str): The title of the blog.

        Returns:
        - bool: True if the blog is favorited by the user,
            False otherwise.
        """
        try:
            blog = self.blog
            user = self.user
        except Blog.DoesNotExist:
            pass

        queryset = Favorite.objects.filter(blog_id=blog, user_id=user)

        if queryset:
            return True
        return False

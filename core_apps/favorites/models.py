from django.contrib.auth import get_user_model
from django.db import models
from typing import Any

from core_apps.articles.models import Blog
from core_apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Favorite(TimeStampedUUIDModel):
    """Favorite model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="favorites")
    article = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="blog_favorites"
    )

    def __str__(self) -> str:
        """Return string representation of the model"""
        return f"{self.user.username} favorited {self.blog.title}"

    def is_favorited(self, user, blog: str) -> bool:
        """Check if blog is favorited by user"""
        try:
            blog = self.blog
            user = self.user
        except Blog.DoesNotExist:
            pass

        queryset = Favorite.objects.filter(blog_id=blog, user_id=user)

        if queryset:
            return True
        return False

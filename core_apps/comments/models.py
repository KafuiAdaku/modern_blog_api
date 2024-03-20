from django.contrib.auth import get_user_model
from django.db import models

from core_apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Comment(TimeStampedUUIDModel):
    """Comment model"""

    blog = models.ForeignKey(
        "blogs.Blog", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey("profiles.Profile", on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self) -> str:
        """Return comment author and blog"""
        return f"{self.author} commented on {self.blog}"

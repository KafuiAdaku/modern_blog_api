from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.blogs.models import Blog
from core_apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class ReactionManager(models.Manager):
    """Custom manager for Reaction model."""

    def likes(self) -> int:
        """Return the number of likes."""
        return self.get_queryset().filter(reaction__gt=0).count()

    def dislikes(self) -> int:
        """Return the number of dislikes."""
        return self.get_queryset().filter(reaction__lt=0).count()

    def has_reacted(self) -> bool:
        """Check if user has reacted."""
        request = self.context.get("request")
        if request:
            self.get_queryset().filter(user=request)


class Reaction(TimeStampedUUIDModel):
    """Model for user reactions on articles."""

    class Reactions(models.IntegerChoices):
        """Choices for user reactions."""

        LIKE = 1, _("like")
        DISLIKE = -1, _("dislike")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="blog_reactions"
    )
    reaction = models.IntegerField(
        verbose_name=_("like-dislike"), choices=Reactions.choices
    )

    objects = ReactionManager()

    class Meta:
        """Meta options."""

        unique_together = ["user", "blog", "reaction"]

    def __str__(self):
        """Return string representation."""
        return f"{self.user.username} voted on \
            {self.blog.title} with a {self.reaction}"

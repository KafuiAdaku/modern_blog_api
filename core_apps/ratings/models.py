from typing import List

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core_apps.common.models import TimeStampedUUIDModel

# Get the user model
User = get_user_model()


class Rating(TimeStampedUUIDModel):
    """
    Model representing a rating for a blog.

    This model represents the rating given by a user to a
        specific blog post.

    Attributes:
    - blog (ForeignKey): The blog being rated.
    - rated_by (ForeignKey): The user who rated the blog.
    - value (IntegerField): The rating value, chosen from
        predefined choices.
    - review (TextField): Optional review provided by the user.
    - Meta (class): Inner class defining metadata options
        for the model.
    """

    class Range(models.IntegerChoices):
        """
        Choices for rating values.

        These choices represent the possible rating
            values for a blog.
        """

        RATING_1 = 1, _("poor")
        RATING_2 = 2, _("fair")
        RATING_3 = 3, _("good")
        RATING_4 = 4, _("very good")
        RATING_5 = 5, _("excellent")

    blog = models.ForeignKey(
        "blogs.Blog", related_name="blog_ratings", on_delete=models.CASCADE
    )
    rated_by = models.ForeignKey(
        User, related_name="user_who_rated", on_delete=models.CASCADE
    )
    value = models.IntegerField(
        verbose_name=_("rating value"),
        choices=Range.choices,
        default=0,
        help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent",
    )
    review = models.TextField(verbose_name=_("rating review"), blank=True)

    class Meta:
        """
        Metadata options for the Rating model.

        Attributes:
        - unique_together (list): Specifies the
            unique-together constraint for the model.
        """

        unique_together: List[str] = ["rated_by", "blog"]

    def __str__(self) -> str:
        """
        Return a string representation of the rating.

        Returns:
        - str: A string representing the blog title
            and the rating value.
        """
        return f"{self.blog.title} rated at {self.value}"

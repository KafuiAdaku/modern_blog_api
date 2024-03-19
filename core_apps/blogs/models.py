from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from typing import List, Union

from core_apps.common.models import TimeStampedUUIDModel
from core_apps.ratings.models import Rating

from .read_time_engine import BlogReadTimeEngine

User = get_user_model()


class Tag(TimeStampedUUIDModel):
    """Tag Model"""
    tag = models.CharField(max_length=80)
    slug = models.SlugField(db_index=True, unique=True)

    class Meta:
        """Meta"""
        ordering = ["tag"]

    def __str__(self) -> str:
        """String Representation"""
        return self.tag


class Blog(TimeStampedUUIDModel):
    """Blog Model"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name=_("user"), related_name="blogs"
    )
    title = models.CharField(verbose_name=_("title"), max_length=250)
    slug = AutoSlugField(populate_from="title",
                         always_update=True, unique=True)
    description = models.CharField(verbose_name=_("description"),
                                   max_length=255)
    body = models.TextField(verbose_name=_("blog content"))
    banner_image = models.ImageField(
        verbose_name=_("banner image"), default="/house_sample.jpg"
    )
    tags = models.ManyToManyField(Tag, related_name="blogs")
    views = models.IntegerField(verbose_name=_("blog views"), default=0)

    def __str__(self):
        """String Representation"""
        return f"{self.author.username}'s article"

    @property
    def list_of_tags(self) -> List[str]:
        """List of Tags"""
        tags = [tag.tag for tag in self.tags.all()]
        return tags

    @property
    def blog_read_time(self) -> int:
        """Blog Read Time"""
        time_to_read = BlogReadTimeEngine(self)
        return time_to_read.get_read_time()

    def get_average_rating(self) -> Union[float, int]:
        """Get Average Rating"""
        if Rating.objects.all().count() > 0:
            rating = (
                Rating.objects.filter(blog=self.pkid).all().
                aggregate(Avg("value"))
            )
            return round(rating["value__avg"], 1) if \
                rating["value__avg"] else 0
        return 0


class BlogViews(TimeStampedUUIDModel):
    """Blog Views"""
    ip = models.CharField(verbose_name=_("ip address"), max_length=250)
    blog = models.ForeignKey(
        Blog, related_name="blog_views", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        """String Representation"""
        return (
            f"Total views on - {self.blog.title} is - \
                {self.blog.views} view(s)"
        )

    class Meta:
        """Meta"""
        verbose_name = "Total views on Blog"
        verbose_name_plural = "Total Blog Views"

from django.utils import timezone
from haystack import indexes
from typing import Any

from core_apps.blogs.models import Blog


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    author = indexes.CharField(model_attr="author")
    title = indexes.CharField(model_attr="title")
    body = indexes.CharField(model_attr="body")
    created_at = indexes.CharField(model_attr="created_at")
    updated_at = indexes.CharField(model_attr="updated_at")

    @staticmethod
    def prepare_author(obj: Blog) -> str:
        """Prepare author."""
        return "" if not obj.author else obj.author.username

    @staticmethod
    def prepare_autocomplete(obj: Blog) -> str:
        """Prepare autocomplete."""
        return " ".join((obj.author.username, obj.title, obj.description))

    def get_model(self):
        """Get model."""
        return Blog

    def index_queryset(self, using: Any = None) -> Blog:
        """Index queryset."""
        return self.get_model().objects.filter(created_at__lte=timezone.now())

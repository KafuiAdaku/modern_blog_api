from typing import Any

from django.utils import timezone
from haystack import indexes

from core_apps.blogs.models import Blog


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Search index for the Blog model.

    This search index defines fields to be indexed for searching
        blog articles.

    Attributes:
    - text (indexes.CharField): Field for the full-text search.
    - author (indexes.CharField): Field for the author's username.
    - title (indexes.CharField): Field for the blog title.
    - body (indexes.CharField): Field for the blog body.
    - created_at (indexes.CharField): Field for the creation date.
    - updated_at (indexes.CharField): Field for the last update date.
    """

    text = indexes.CharField(document=True)
    author = indexes.CharField(model_attr="author")
    title = indexes.CharField(model_attr="title")
    body = indexes.CharField(model_attr="body")
    created_at = indexes.CharField(model_attr="created_at")
    updated_at = indexes.CharField(model_attr="updated_at")

    @staticmethod
    def prepare_author(obj: Blog) -> str:
        """
        Prepare the author's username for indexing.

        Args:
        - obj (Blog): The Blog object.

        Returns:
        - str: The username of the author.
        """
        return "" if not obj.author else obj.author.username

    @staticmethod
    def prepare_autocomplete(obj: Blog) -> str:
        """
        Prepare autocomplete fields for indexing.

        Args:
        - obj (Blog): The Blog object.

        Returns:
        - str: Concatenated string of username, title,
            and description for autocomplete.
        """
        return " ".join((obj.author.username, obj.title, obj.description))

    def get_model(self):
        """
        Get the model for indexing.

        Returns:
        - Blog: The Blog model.
        """
        return Blog

    def index_queryset(self, using: Any = None) -> Blog:
        """
        Get the queryset for indexing.

        Args:
        - using (Any): The database alias.

        Returns:
        - QuerySet: The queryset of Blog objects to be indexed.
        """
        return self.get_model().objects.filter(created_at__lte=timezone.now())

import uuid
from django.db import models

# features that would be available in all models


class TimeStampedUUIDModel(models.Model):
    """
    Abstract base model providing timestamp and UUID fields.

    This model defines common fields that would be available in all models
    requiring creation and update timestamps along with a UUID primary key.

    Attributes:
    - pkid (BigAutoField): Primary key field.
    - id (UUIDField): Unique identifier field.
    - created_at (DateTimeField): Timestamp for creation.
    - updated_at (DateTimeField): Timestamp for last update.

    Meta:
    - abstract (bool): Indicates that this model is abstract and should not be
        created as a separate database table.
    - ordering (list): Specifies the default ordering for queries on this model.
    """

    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract: bool = True
        ordering: list = ["-created_at", "-updated_at"]

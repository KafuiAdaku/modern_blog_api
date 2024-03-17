import logging
from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from modern_blog_api.settings.base import AUTH_USER_MODEL
from core_apps.profiles.models import Profile

logger: logging.Logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(
    sender: Any, instance: Any, created: bool, **kwargs: Any
) -> None:
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender: Any, instance: Any, **kwargs: Any) -> None:
    instance.profile.save()
    logger.info(f"{instance}'s profile created")

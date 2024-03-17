import logging
from typing import Any

import random
from django.db.models.signals import post_save
from django.dispatch import receiver

from modern_blog_api.settings.base import AUTH_USER_MODEL
from core_apps.profiles.models import Profile

logger: logging.Logger = logging.getLogger(__name__)


def get_default_profile_image_url() -> str:
    profile_imgs_collections_list = [
        "notionists-neutral",
        "adventurer-neutral",
        "fun-emoji",
        "big-ears-neutral",
        "initials",
    ]
    profile_imgs_name_list = [
        "Garfield",
        "Tinkerbell",
        "Annie",
        "Loki",
        "Cleo",
        "Angel",
        "Bob",
        "Mia",
        "Coco",
        "Gracie",
        "Bear",
        "Bella",
        "Abby",
        "Harley",
        "Cali",
        "Leo",
        "Luna",
        "Jack",
        "Felix",
        "Kiki",
    ]

    collection = random.choice(profile_imgs_collections_list)
    name = random.choice(profile_imgs_name_list)

    return f"https://api.dicebear.com/8.x/{collection}/svg?seed={name}"


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(
    sender: Any, instance: Any, created: bool, **kwargs: Any
) -> None:
    if created:
        profile = Profile.objects.create(user=instance)

        if not profile.profile_photo:
            profile.profile_photo = get_default_profile_image_url()
            profile.save()


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender: Any, instance: Any, **kwargs: Any) -> None:
    instance.profile.save()
    logger.info(f"{instance}'s profile created")

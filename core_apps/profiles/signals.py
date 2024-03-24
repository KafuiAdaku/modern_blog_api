import logging
import random
from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from core_apps.profiles.models import Profile
from modern_blog_api.settings.base import AUTH_USER_MODEL

# Setting up logging
logger: logging.Logger = logging.getLogger(__name__)


def get_default_profile_image_url() -> str:
    """
    Generates a URL for a default profile image.

    Returns:
    - str: URL for the default profile image.
    """
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


# Signal to create a profile for a newly created user
@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(
    sender: Any, instance: Any, created: bool, **kwargs: Any
) -> None:
    """
    Creates a profile for a newly created user.

    Args:
    - sender (Any): The sender of the signal.
    - instance (Any): The instance triggering the signal.
    - created (bool): Indicates if the instance is newly created.
    - **kwargs (Any): Additional keyword arguments.
    """
    if created:
        profile = Profile.objects.create(user=instance)

        if not profile.profile_photo:
            profile.profile_photo = get_default_profile_image_url()
            profile.save()


# Signal to save the profile when the user is saved
@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender: Any, instance: Any, **kwargs: Any) -> None:
    """
    Saves the profile when the user is saved.

    Args:
    - sender (Any): The sender of the signal.
    - instance (Any): The instance triggering the signal.
    - **kwargs (Any): Additional keyword arguments.
    """
    instance.profile.save()
    logger.info(f"{instance}'s profile created")

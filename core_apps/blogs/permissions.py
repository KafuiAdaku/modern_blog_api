from typing import Any

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to
        edit it.

    This permission class checks if the user making the
        request is the owner
    of the object they are trying to edit or delete.
    """

    message = "You are not allowed to update or \
        delete an blog that does not belong to you"

    def has_object_permission(self, request: Any, view: Any, obj: Any) -> bool:
        """
        Check if the user is the author of the blog post.

        Args:
        - request (Any): The request being made.
        - view (Any): The view being accessed.
        - obj (Any): The object being accessed.

        Returns:
        - bool: True if the user is the author of the blog post,
            False otherwise.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user

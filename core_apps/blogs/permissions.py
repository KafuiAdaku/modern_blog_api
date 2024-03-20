from rest_framework import permissions
from typing import Any


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""

    message = "You are not allowed to update or \
        delete an blog that does not belong to you"

    def has_object_permission(self, request: Any, view: Any, obj: Any) -> bool:
        """Check if user is the author of the blog post"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user

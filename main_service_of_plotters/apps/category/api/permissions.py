"""This module contains custom permissions."""

from rest_framework.permissions import BasePermission


class AdministratorPermission(BasePermission):
    """This class contains permissions for administrator."""

    def has_permission(self, request, view) -> bool:
        """Return `True` if permission is granted, `False` otherwise."""
        if request.user.is_administrator() or request.user.is_superuser:
            return True
        return False

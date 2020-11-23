"""API permissions set."""

from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):
    """Permission check if loggined user have `User` role."""

    def has_permission(self, request, view):
        if request.user.is_user():
            return False
        return True

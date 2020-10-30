from rest_framework.permissions import BasePermission


class AdministratorPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_administrator() or request.user.is_superuser:
            return True
        return False

from rest_framework.permissions import SAFE_METHODS, BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_user():
            return False
        return True

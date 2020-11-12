from rest_framework.permissions import SAFE_METHODS, BasePermission


class PlotterUserPermission(BasePermission):
    """Permission check request user to iteracte with plotters."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS) or request.user.is_dealer() \
               or request.user.is_administrator() or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return (request.user.is_user() and obj.user == request.user) or \
               (request.user.is_dealer() and obj.dealer == request.user) or \
               request.user.is_administrator() or request.user.is_superuser

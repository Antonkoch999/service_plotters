from rest_framework.permissions import SAFE_METHODS, BasePermission


class PlotterUserPermission(BasePermission):
    """Permission check request user to iteracte with plotters."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_dealer() or \
                request.user.is_administrator() or \
                request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.user.is_user():
            return obj.user == request.user
        elif request.user.is_dealer():
            return obj.dealer == request.user
        elif request.user.is_administrator():
            return True
        else:
            return request.user.is_superuser

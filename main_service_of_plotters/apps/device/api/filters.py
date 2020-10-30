from rest_framework.filters import BaseFilterBackend


class IsUserOwnFilter(BaseFilterBackend):
    """Check if user is `User` and filtering only instances its own."""

    def filter_queryset(self, request, queryset, view):
        if request.user.is_user():
            return queryset.filter(user=request.user)
        else:
            return queryset


class IsDealerOwnFilter(BaseFilterBackend):
    """Check if user is `Dealer` and filtering only instances its own."""

    def filter_queryset(self, request, queryset, view):
        if request.user.is_dealer():
            return queryset.filter(dealer=request.user)
        else:
            return queryset

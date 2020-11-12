from rest_framework.filters import BaseFilterBackend


class IsUserOwnFilter(BaseFilterBackend):
    """Check if user is `User` and filtering only instances its own."""

    def filter_queryset(self, request, queryset, view):
        if request.user.is_user():
            filter_qs = queryset.filter(user=request.user)
        else:
            filter_qs = queryset
        return filter_qs


class IsDealerOwnFilter(BaseFilterBackend):
    """Check if user is `Dealer` and filtering only instances its own."""

    def filter_queryset(self, request, queryset, view):
        if request.user.is_dealer():
            filter_qs = queryset.filter(dealer=request.user)
        else:
            filter_qs = queryset
        return filter_qs

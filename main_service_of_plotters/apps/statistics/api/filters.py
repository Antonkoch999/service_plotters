from rest_framework.filters import BaseFilterBackend


class IsUserPlotterOwnFilter(BaseFilterBackend):
    """Check if user is `User` and filtering only instances its own."""

    def filter_queryset(self, request, queryset, view):
        if request.user.is_user():
            return queryset.filter(plotter__user=request.user)
        else:
            return queryset


class IsDealerPlotterOwnFilter(BaseFilterBackend):
    """Check if user is `Dealer` and filtering only instances its own."""

    def filter_queryset(self, request, queryset, view):
        if request.user.is_dealer():
            return queryset.filter(plotter__dealer=request.user)
        else:
            return queryset

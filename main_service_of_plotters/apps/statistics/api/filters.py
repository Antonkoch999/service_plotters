"""This module contains custom filter."""

from rest_framework.filters import BaseFilterBackend


class IsUserPlotterOwnFilter(BaseFilterBackend):
    """Check if user is `User` and filtering only instances its own."""

    def filter_queryset(self, request, queryset, view):
        """Return queryset depending on the user group."""
        if request.user.is_user():
            qs = queryset.filter(plotter__user=request.user)
        else:
            qs = queryset
        return qs


class IsDealerPlotterOwnFilter(BaseFilterBackend):
    """Check if user is `Dealer` and filtering only instances its own."""

    def filter_queryset(self, request, queryset, view):
        """Return queryset depending on the user group."""
        if request.user.is_dealer():
            qs = queryset.filter(plotter__dealer=request.user)
        else:
            qs = queryset
        return qs

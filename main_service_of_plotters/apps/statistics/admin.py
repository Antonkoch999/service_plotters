"""This class is representation of statistics in the admin interface."""

from django.contrib import admin

from .models import CuttingTransaction, StatisticsPlotter, StatisticsTemplate
from .forms import StatisticsPlotterFrom, StatisticsPlotterFromUserDealer


class TemplateAdmin(admin.ModelAdmin):
    """Class representation of model statistics template in interface admin."""

    list_display = ['plotter', 'template', 'count']

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


class PlotterAdmin(TemplateAdmin):
    """Class representation of model statistics plotter in interface admin."""

    form = StatisticsPlotterFrom
    list_display = ['plotter', 'ip', 'last_request',
                    'count_cut', 'date_creation', 'date_update']

    def get_form(self, request, obj=None, **kwargs):
        """Change form of admin page depended of logged user."""

        if PlotterAdmin._is_requested_user_dealer_or_user(request):
            kwargs['form'] = StatisticsPlotterFromUserDealer
        return super().get_form(request, obj, **kwargs)

    def get_list_display(self, request):
        """Change list_display list depended of logged user."""

        # If user is `Dealer` or User
        if PlotterAdmin._is_requested_user_dealer_or_user(request):
            # without `ip`
            return ['plotter', 'last_request',
                    'count_cut', 'date_creation', 'date_update']
        return super().get_list_display(request)

    @staticmethod
    def _is_requested_user_dealer_or_user(request):
        """Helper method identificate is authenticated user is dealer."""

        return request.user.groups.filter(name='Dealer').exists() \
            or request.user.groups.filter(name='User').exists()


class CuttingAdmin(TemplateAdmin):
    """Class representation of model statistics journal in interface admin."""

    list_display = ['user', 'plotter', 'template', 'date_cutted']

    def get_queryset(self, request):
        """Changes QuerySet model instance depending of the user groups."""

        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Dealer').exists():
            return qs.filter(user__dealer_id=request.user.pk)
        return qs


admin.site.register(StatisticsTemplate, TemplateAdmin)
admin.site.register(StatisticsPlotter, PlotterAdmin)
admin.site.register(CuttingTransaction, CuttingAdmin)

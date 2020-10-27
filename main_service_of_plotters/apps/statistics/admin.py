"""This class is representation of statistics in the admin interface."""

from django.contrib import admin

from .models import CuttingTransaction, StatisticsPlotter, StatisticsTemplate


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

    list_display = ['plotter', 'ip', 'last_request',
                    'count_cut', 'date_creation', 'date_update']


class CuttingAdmin(TemplateAdmin):
    """Class representation of model statistics journal in interface admin."""

    list_display = ['user', 'plotter', 'template', 'label', 'date_cutted']

    def get_queryset(self, request):
        """Changes QuerySet model instance depending of the user groups."""

        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Dealer').exists():
            return qs.filter(user__dealer_id=request.user.pk)
        return qs


admin.site.register(StatisticsTemplate, TemplateAdmin)
admin.site.register(StatisticsPlotter, PlotterAdmin)
admin.site.register(CuttingTransaction, CuttingAdmin)

from django.contrib import admin

from .models import StatisticsPlotter, StatisticsTemplate, CuttingTransaction


class TemplateAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
                    StatisticsTemplate._meta.get_fields()]

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
    list_display = ['plotter_id', 'IP', 'last_request',
                    'count_cut', 'date_creation', 'date_update']


class CuttingAdmin(TemplateAdmin):
    list_display = [field.name for field in
                    CuttingTransaction._meta.get_fields()]


admin.site.register(StatisticsTemplate, TemplateAdmin)
admin.site.register(StatisticsPlotter, PlotterAdmin)
admin.site.register(CuttingTransaction, CuttingAdmin)

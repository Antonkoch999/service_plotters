from django.contrib import admin

from main_service_of_plotters.apps.device.models import Plotter


class PlotterAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'user', )


admin.site.register(Plotter, PlotterAdmin)


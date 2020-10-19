from django.contrib import admin
from main_service_of_plotters.apps.statistics.models import StatisticsTemplate, \
    StatisticsPlotter
# Register your models here.

admin.site.register(StatisticsTemplate)
admin.site.register(StatisticsPlotter)

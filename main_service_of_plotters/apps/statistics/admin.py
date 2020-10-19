from django.contrib import admin

from .models import StatisticsPlotter, StatisticsTemplate

admin.site.register(StatisticsTemplate)
admin.site.register(StatisticsPlotter)

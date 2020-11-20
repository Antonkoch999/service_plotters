"""This class is representation of category in the admin interface."""

from django.contrib import admin

from main_service_of_plotters.apps.category.models import Manufacturer, \
    DeviceCategory, ModelsTemplate

admin.site.register(Manufacturer)
admin.site.register(DeviceCategory)
admin.site.register(ModelsTemplate)

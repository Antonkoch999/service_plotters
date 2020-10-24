from django.contrib import admin

from main_service_of_plotters.apps.category.models import Manufacturer, \
    DeviceCategory


admin.site.register(Manufacturer)
admin.site.register(DeviceCategory)

from django.db import models
from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate


class DeviceCategory(DateTimeDateUpdate):
    name = models.CharField(max_length=150, blank=True,
                            verbose_name='Name of template device')

    def __str__(self):
        return f'Category {self.name}'


class Manufacturer(DateTimeDateUpdate):
    device_category = models.ForeignKey(DeviceCategory,
                                        on_delete=models.CASCADE,
                                        verbose_name='Instance model device')
    name = models.CharField(max_length=150, blank=True,
                            verbose_name='Name of template manufacturer')

    def __str__(self):
        return f'Category {self.device_category.name} | Manufacturer {self.name}'

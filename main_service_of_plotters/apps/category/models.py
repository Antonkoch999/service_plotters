from django.db import models
from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate


class DeviceCategory(DateTimeDateUpdate):
    name = models.CharField(max_length=150, blank=True,
                            verbose_name='Name of template device')
    photo = models.ImageField(upload_to="device/%Y/%m/%d",
                              verbose_name='Photo Device', blank=True,
                              null=True)

    def __str__(self):
        return f'Category {self.name}'


class Manufacturer(DateTimeDateUpdate):
    device_category = models.ForeignKey(DeviceCategory,
                                        on_delete=models.CASCADE,
                                        verbose_name='Instance model device')
    name = models.CharField(max_length=150, blank=True,
                            verbose_name='Name of template manufacturer')
    photo = models.ImageField(upload_to="manufacturer/%Y/%m/%d",
                              verbose_name='Photo manufacturer', blank=True,
                              null=True)

    def __str__(self):
        return f'Category {self.device_category.name} | Manufacturer {self.name}'


class ModelsTemplate(DateTimeDateUpdate):
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        verbose_name='Instance model manufacturer',
    )
    name = models.CharField(max_length=150, blank=True,
                            verbose_name='Name of model template')

    def __str__(self):
        return f'Category {self.manufacturer.device_category.name} | Manufacturer {self.manufacturer.name} | Model {self.name}'

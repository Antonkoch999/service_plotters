"""This module creates tables in the database."""

from django.db import models
from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate
from django.utils.translation import gettext_lazy as _


class DeviceCategory(DateTimeDateUpdate):
    """Create table device category in the database."""

    name = models.CharField(max_length=150, blank=True,
                            verbose_name=_('Name of category of devices'))
    photo = models.ImageField(upload_to="device/%Y/%m/%d",
                              verbose_name=_('Photo Device'), blank=True,
                              null=True)

    def __str__(self):
        return _('Category') + f' {self.name}'


class Manufacturer(DateTimeDateUpdate):
    """Create table manufacturer in the database."""

    device_category = models.ForeignKey(DeviceCategory,
                                        on_delete=models.CASCADE,
                                        verbose_name=_('Category of devices'),
                                        related_name='device')
    name = models.CharField(max_length=150, blank=True,
                            verbose_name=_('Name of manufacturer'))
    photo = models.ImageField(upload_to="manufacturer/%Y/%m/%d",
                              verbose_name=_('Manufacturer image'), blank=True,
                              null=True)

    def __str__(self):
        return f'{_("Category")} {self.device_category.name} | ' \
               f'{_("Manufacturer")} {self.name}'


class ModelsTemplate(DateTimeDateUpdate):
    """Create table models template in the database."""

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        verbose_name=_('Manufacturer'),
        related_name='modelstemplate'
    )
    name = models.CharField(max_length=150, blank=True,
                            verbose_name=_('Name of model'))

    def __str__(self):
        return f'Category {self.manufacturer.device_category.name} | ' \
               f'Manufacturer {self.manufacturer.name} | Model {self.name}'

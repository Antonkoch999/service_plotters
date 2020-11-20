"""This module creates tables in the database."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate


class DeviceCategory(DateTimeDateUpdate):
    """Create table device category in the database."""

    name = models.CharField(max_length=150, blank=True,
                            verbose_name=_('Name'),
                            help_text=_('Name of category of devices'))
    photo = models.ImageField(upload_to="device/%Y/%m/%d",
                              verbose_name=_('Photo'), blank=True,
                              null=True,
                              help_text=_('Photo of category of devices'))

    class Meta:
        """Metadata of models DeviceCategory."""

        verbose_name = _("Device category")
        verbose_name_plural = _("Device categories")

    def __str__(self) -> str:
        """Return the string representation of the object.

        :return: string format: Category name
        """
        return _('Category') + f' {self.name}'


class Manufacturer(DateTimeDateUpdate):
    """Create table manufacturer in the database."""

    device_category = models.ForeignKey(DeviceCategory,
                                        on_delete=models.CASCADE,
                                        verbose_name=_('Category of devices'),
                                        related_name='device',)
    name = models.CharField(max_length=150, blank=True,
                            verbose_name=_('Name'),
                            help_text=_('Name of manufacturer'))
    photo = models.ImageField(upload_to="manufacturer/%Y/%m/%d",
                              verbose_name=_('Photo'), blank=True,
                              null=True, help_text=_('Photo of manufacturer'))

    class Meta:
        """Metadata of models Manufacturer."""

        verbose_name = _("Manufacturer")
        verbose_name_plural = _("Manufacturers")

    def __str__(self) -> str:
        """Return the string representation of the object.

        :return: string format: Category name | Manufacturer name
        """
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
                            verbose_name=_('Name'),
                            help_text=_('Name of models template'))

    class Meta:
        """Metadata of models ModelsTemplate."""

        verbose_name = _("Model")
        verbose_name_plural = _("Models")

    def __str__(self) -> str:
        """Return the string representation of the object.

        :return: string format: Category name | Manufacturer name| Model name
        """
        return f'Category {self.manufacturer.device_category.name} | ' \
               f'Manufacturer {self.manufacturer.name} | Model {self.name}'

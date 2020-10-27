"""This module creates tables in database."""

from django.db import models

from .validators import validate_unique_code, \
    validate_file_photo, validate_file_plt

from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate
from main_service_of_plotters.apps.category.models import DeviceCategory, \
    Manufacturer, ModelsTemplate
from main_service_of_plotters.apps.users.models import User


class Template(DateTimeDateUpdate):
    """This class creates template table."""

    device_category = models.ForeignKey(DeviceCategory,
                                        on_delete=models.CASCADE,
                                        verbose_name='Name of template device',
                                        null=True, blank=True
                                        )
    manufacturer_category = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        verbose_name='Name of template manufacturer', null=True, blank=True
    )
    model_category = models.ForeignKey(ModelsTemplate,
                                       on_delete=models.CASCADE,
                                       verbose_name='Name of template model',
                                       null=True, blank=True)
    name = models.CharField(max_length=100, blank=True,
                            verbose_name='name of template')
    file_photo = models.FileField(upload_to="photo/%Y/%m/%d",
                                  verbose_name='Upload file with photo',
                                  validators=[validate_file_photo])
    file_plt = models.FileField(upload_to="documents/%Y/%m/%d",
                                verbose_name='Upload file format .plt',
                                validators=[validate_file_plt])

    def __str__(self):
        return f'Template {self.name}'


class Label(DateTimeDateUpdate):
    """This class creates label table."""

    scratch_code = models.CharField(max_length=16, blank=True,
                                    validators=[validate_unique_code],
                                    verbose_name='Unique scratch code')
    barcode = models.CharField(max_length=16, blank=True,
                               validators=[validate_unique_code],
                               verbose_name='Unique barcode')
    count = models.IntegerField(default=0)
    dealer = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='instance model Dealer',
                               limit_choices_to={'role': 'Dealer'},
                               null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='instance model User',
                             limit_choices_to={'role': 'User'},
                             related_name='label_user', null=True, blank=True)

    class Meta:
        unique_together = [['scratch_code', 'barcode']]

    def __str__(self):
        return f'Scratch code {self.scratch_code}'

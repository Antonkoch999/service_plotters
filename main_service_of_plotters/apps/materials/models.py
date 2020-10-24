from django.db import models
from django.utils.timezone import now

from .validators import validate_unique_code

from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate
# from main_service_of_plotters.apps.users.constants import CATEGORY
from main_service_of_plotters.apps.category.models import DeviceCategory, Manufacturer


class Template(DateTimeDateUpdate):
    """This class creates template table."""
    # CATEGORY_OF_TEMPLATE = ((CATEGORY[key], key) for key in
    #                         CATEGORY.keys())
    # category = models.CharField(max_length=60, blank=True,
    #                             verbose_name='category template',
    #                             choices=CATEGORY_OF_TEMPLATE
    #                             )
    device_category = models.ForeignKey(DeviceCategory,
                                        on_delete=models.CASCADE,
                                        verbose_name='Name of template device'
                                        )
    manufacturer_category = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        verbose_name='Name of template manufacturer',
    )
    name = models.CharField(max_length=100, blank=True,
                            verbose_name='name of template')
    file_photo = models.FileField(verbose_name='Upload file with photo')
    file_plt = models.FileField(verbose_name='Upload file format .plt')

    def __str__(self):
        return f'Template {self.name}'


class Label(DateTimeDateUpdate):
    """This class creates label table."""
    #
    # template = models.ForeignKey(Template, on_delete=models.CASCADE,
    #                              verbose_name='instance model template')
    scratch_code = models.CharField(max_length=16, blank=True,
                                    validators=[validate_unique_code],
                                    verbose_name='Unique scratch code')
    barcode = models.CharField(max_length=16, blank=True,
                               validators=[validate_unique_code],
                               verbose_name='Unique barcode')
    # date_life = models.DateField(verbose_name='Lifetime of label')
    count = models.IntegerField(default=0)

    # lot = models.IntegerField()
    # size = models.CharField(max_length=150, blank=True,
    #                         verbose_name='Size of label')

    class Meta:
        unique_together = [['scratch_code', 'barcode']]

    def __str__(self):
        return f'Scratch code {self.scratch_code}'

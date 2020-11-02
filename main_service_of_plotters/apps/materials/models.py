"""This module creates tables in database."""
from datetime import timedelta
from django.utils.timezone import now

from django.db import models
from django.urls import reverse

from .validators import validate_unique_code, \
    validate_file_photo, validate_file_plt
from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate
from main_service_of_plotters.apps.category.models import DeviceCategory, \
    Manufacturer, ModelsTemplate
from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.apps.device.models import Plotter


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
                                       null=True, blank=True, )
    name = models.CharField(max_length=100, blank=True,
                            verbose_name='name of template')
    file_photo = models.FileField(upload_to="photo/%Y/%m/%d",
                                  verbose_name='Upload file with photo',
                                  validators=[validate_file_photo])
    file_plt = models.FileField(upload_to="documents/%Y/%m/%d",
                                verbose_name='Upload file format .plt',
                                validators=[validate_file_plt])

    def get_absolute_url(self) -> str:
        return reverse('api:template-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Template {self.name}'


class Label(DateTimeDateUpdate):
    """This class creates label table."""
    TERM_OF_EXPIRATION = timedelta(days=90)

    scratch_code = models.CharField(max_length=16, blank=True,
                                    validators=[validate_unique_code],
                                    verbose_name='Unique scratch code')
    barcode = models.CharField(max_length=16, blank=True,
                               validators=[validate_unique_code],
                               verbose_name='Unique barcode')
    count = models.IntegerField(default=0)
    available_count = models.IntegerField(default=0)
    dealer = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='instance model Dealer',
                               limit_choices_to={'role': 'Dealer'},
                               null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='instance model User',
                             limit_choices_to={'role': 'User'},
                             related_name='label_user', null=True, blank=True)

    date_of_activation = models.DateTimeField(
        null=True,
        default=None
    )
    linked_plotter = models.ForeignKey(
        Plotter,
        null=True,
        default=None,
        related_name='linked_labels',
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = [['scratch_code', 'barcode']]

    def get_absolute_url(self) -> str:
        return reverse('api:label-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Scratch code {self.scratch_code}'

    @property
    def date_of_expiration(self):
        if self.date_of_activation is not None:
            return self.date_creation + self.TERM_OF_EXPIRATION
        else:
            return None

    @property
    def days_before_expiration(self):
        if self.date_of_expiration:
            expiration_term = self.date_of_expiration - now()
            return f"{expiration_term.days} days"

    @property
    def is_in_terms_of_expiration(self):
        if self.date_of_activation:
            return self.date_of_activation < now() and \
                now() < self.date_of_expiration
        else:
            return False

    @property
    def is_active_and_not_expired(self):
        return self.is_active and self.is_in_terms_of_expiration

    def link_to_plotter(self, plotter):
        self.linked_plotter = plotter
        self.date_of_activation = now()
        self.is_active = True
        self.available_count = self.count
        self.save()

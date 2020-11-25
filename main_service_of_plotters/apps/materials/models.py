"""This module creates tables in database."""
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.urls import reverse

from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate
from main_service_of_plotters.apps.category.models import DeviceCategory, \
    Manufacturer, ModelsTemplate
from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.materials.constants import SIZE, TERM_OF_EXPIRATION
from .validators import validate_unique_code, \
    validate_file_photo, validate_file_plt


class Template(DateTimeDateUpdate):
    """Representation of `Template` model."""

    SIZE_TEMPLATE = tuple(SIZE.items())
    device_category = models.ForeignKey(
        DeviceCategory,
        on_delete=models.CASCADE,
        verbose_name=_('Category of devices'),
        null=True, blank=True,
        help_text=_("The type of device of template (phone, tablet, etc.)")
    )
    manufacturer_category = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        verbose_name=_('Manufacturer of the model'),
        null=True, blank=True,
        help_text=_("Manufacturer of device of template (Apple, Samsung, etc.)")
    )
    model_category = models.ForeignKey(
        ModelsTemplate,
        on_delete=models.CASCADE,
        verbose_name=_('Model of device'),
        null=True, blank=True,
        help_text=_("Name of device tempalte created for."))
    name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Name of template')
    )
    file_photo = models.FileField(
        upload_to="photo/%Y/%m/%d",
        verbose_name=_('Image'),
        validators=[validate_file_photo],
        help_text=_('File of schematic image of template')
    )
    file_plt = models.FileField(
        upload_to="documents/%Y/%m/%d",
        verbose_name=_('Blueprint file (*.plt)'),
        validators=[validate_file_plt])
    size = models.CharField(
        max_length=1,
        choices=SIZE_TEMPLATE,
        verbose_name=_('Size'),
        blank=True, null=True,
        help_text=_('This is size, points to size of template')
    )

    class Meta:
        """Metadata of Template model."""

        verbose_name = _("Template")
        verbose_name_plural = _("Templates")

    def get_absolute_url(self) -> str:
        """Return URL to template."""
        return reverse('api:template-detail', kwargs={'pk': self.pk})

    def __str__(self):
        """Return string representation of url."""
        return f'{_("Template")} {self.name}'


class Label(DateTimeDateUpdate):
    """This class creates label table."""

    scratch_code = models.CharField(
        max_length=16,
        validators=[validate_unique_code],
        verbose_name=_('Unique scratch code'),
        unique=True,
        help_text=_('Scratch code is secret key what user scratch from '
                    'labels and put to system. Then system activate this '
                    'label')
    )
    barcode = models.CharField(
        max_length=16,
        validators=[validate_unique_code],
        verbose_name=_('Unique barcode'),
        unique=True,
        help_text=_('Identification number of label/')
    )
    count = models.IntegerField(
        default=0,
        verbose_name=_("Start amount"),
        help_text=_('Amount of labels in pack on the start')
    )
    available_count = models.IntegerField(
        default=0, blank=True,
        verbose_name=_("Available amount"),
        help_text=_("Remaining labels in pack.")
    )
    dealer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Related Dealer'),
        limit_choices_to={'role': 'Dealer'},
        null=True, blank=True,
        help_text=_('Dealer who supplies this labels pack.')
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Related User'),
        limit_choices_to={'role': 'User'},
        related_name='label_user',
        null=True, blank=True,
        help_text=_('User who buy this pack of label.')
    )

    date_of_activation = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('Date of activation'),
        help_text=_('Date then user activate this label in plotter.')
    )
    linked_plotter = models.ForeignKey(
        Plotter,
        null=True,
        blank=True,
        related_name='linked_labels',
        on_delete=models.CASCADE,
        verbose_name=_('Linked plotters'),
        help_text=_('The plotter on which the film was activated by user')

    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_('Is active'),
        help_text=_('Show what label was activated early')
    )

    class Meta:
        """Metadata of Label model."""

        verbose_name = _("Label")
        verbose_name_plural = _("Labels")

    def get_absolute_url(self) -> str:
        """Return url to label instance."""
        return reverse('api:label-detail', kwargs={'pk': self.pk})

    def __str__(self):
        """Return string representation of label instance."""
        return f'{_("Scratch code")} {self.scratch_code}'

    def date_of_expiration(self):
        """Calculate date of expiretion from date of activation and constant term."""
        if self.date_of_activation is not None:
            return self.date_of_activation + TERM_OF_EXPIRATION
        return None
    date_of_expiration.short_description = _("Date of expiration")

    def days_before_expiration(self):
        """Calculate days before date of expiration until now."""
        if self.date_of_expiration():
            expiration_term = (self.date_of_expiration() - now()).days
            return expiration_term
        return None
    days_before_expiration.short_description = _("Days before expiration")

    def is_in_terms_of_expiration(self):
        """Check if instance in terms of expiration."""
        if self.date_of_activation:
            return self.date_of_activation < now() and \
                   now() < self.date_of_expiration()
        return False

    @property
    def is_active_and_not_expired(self):
        """Check if instance is active and in terms of expiration."""
        return self.is_active and self.is_in_terms_of_expiration()

    def link_to_plotter(self, plotter):
        """Create link between instance and plotter."""
        self.linked_plotter = plotter
        self.date_of_activation = now()
        self.is_active = True
        self.available_count = self.count
        self.save()

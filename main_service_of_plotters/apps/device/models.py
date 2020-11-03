from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate


class Plotter(DateTimeDateUpdate):
    """This class creates plotter table."""

    dealer = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name=_('Dealer'),
                               limit_choices_to={'role': 'Dealer'},
                               null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name=_('User'),
                             limit_choices_to={'role': 'User'},
                             related_name='plotter_user',
                             null=True, blank=True)
    # FIXME Serial Number must be char string in production stage
    serial_number = models.BigIntegerField(
        verbose_name=_("Serial number")
    )

    available_film = models.BigIntegerField(verbose_name=_("Available film"))

    def available_films(self):
        return sum(label.available_count
                   for label
                   in self.linked_labels.all()
                   if label.is_active_and_not_expired)
    available_films.short_description = _("Available films")

    def __str__(self):
        return f'{_("Plotter")} {self.serial_number}'

    def get_absolute_url(self) -> str:
        return reverse('api:plotter-detail', kwargs={'pk': self.pk})

    def link_label(self, label):
        """Create link to the label."""

        label.link_to_plotter(self)

    @property
    def first_linked_label(self):
        """Return first linked label with positive amount of films, active and not expiered."""

        qs = self.linked_labels.filter(available_count__gt=0).order_by(
            'date_of_activation')
        return [label for label in qs.all() if
                label.is_active_and_not_expired][0]

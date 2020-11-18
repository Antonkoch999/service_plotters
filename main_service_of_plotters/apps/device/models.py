import random

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate


def random_string():
    return str(random.random)[:15]


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
    serial_number = models.CharField(
        _("Serial number"),
        max_length=16,
        blank=False,
        unique=True,
        help_text=_("Serial numbuer of plotter (typicaly printed on label)")
    )
    available_film = models.IntegerField(default=0)
    device_id = models.CharField(
        max_length=15,
    )

    class Meta:
        verbose_name = _("Plotter")
        verbose_name_plural = _("Plotters")

    def available_films(self):
        """Get total of available films."""

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

    def cut_amount(self):
        print(self.statisticsplotter_set.all().aggregate(
            models.Sum('count_cut')))
        return self.statisticsplotter_set.all().aggregate(
            models.Sum('count_cut'))['count_cut__sum']

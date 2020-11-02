from django.db import models
from django.urls import reverse

from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate


class Plotter(DateTimeDateUpdate):
    """This class creates plotter table."""

    dealer = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='instance model Dealer',
                               limit_choices_to={'role': 'Dealer'},
                               null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='instance model User',
                             limit_choices_to={'role': 'User'},
                             related_name='plotter_user', null=True, blank=True)
    # FIXME Serial Number must be char string in production stage
    serial_number = models.BigIntegerField()

    available_film = models.BigIntegerField()

    @property
    def available_films(self):
        return sum(label.available_count
                   for label
                   in self.linked_labels.all()
                   if label.is_active_and_not_expired)

    def __str__(self):
        return f'Plotter {self.serial_number}'

    def get_absolute_url(self) -> str:
        return reverse('api:plotter-detail', kwargs={'pk': self.pk})

    def link_label(self, label):
        label.link_to_plotter(self)

    @property
    def first_linked_label(self):
        qs = self.linked_labels.\
                filter(available_count__gt=0).\
                order_by('date_of_activation')
        return [label for label in qs.all() if label.is_active_and_not_expired][0]

from django.db import models

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
    serial_number = models.BigIntegerField()
    available_film = models.IntegerField(default=0)

    def __str__(self):
        return f'Plotter {self.serial_number}'

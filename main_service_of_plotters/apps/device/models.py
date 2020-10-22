from django.db import models

from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate


class Plotter(DateTimeDateUpdate):
    """This class creates plotter table."""

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='instance model User')
    serial_number = models.BigIntegerField()

    def __str__(self):
        return f'Plotter {self.serial_number}'

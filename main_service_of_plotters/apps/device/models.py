from django.db import models
from main_service_of_plotters.apps.users.models import User


class Plotter(models.Model):
    """This class creates plotter table."""

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='instance model User')
    serial_number = models.BigIntegerField()

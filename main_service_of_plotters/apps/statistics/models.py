from django.db import models
from django.utils.timezone import now

from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.materials.models import Template
from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.apps.materials.models import Label
from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate


class StatisticsPlotter(DateTimeDateUpdate):
    """This class creates a plotter statistics table in the database."""

    plotter = models.ForeignKey(Plotter, on_delete=models.CASCADE,
                                verbose_name='instance model plotter')
    ip = models.CharField(max_length=150, verbose_name='IP address plotter')
    last_request = models.DateField(verbose_name='last connection to server')
    count_cut = models.IntegerField()


class StatisticsTemplate(DateTimeDateUpdate):
    """This class creates a template statistics table in the database."""

    plotter = models.ForeignKey(Plotter, on_delete=models.CASCADE,
                                verbose_name='instance model plotter')
    template = models.ForeignKey(Template, on_delete=models.CASCADE,
                                 verbose_name='instance model template')
    count = models.IntegerField()


class CuttingTransaction(DateTimeDateUpdate):
    """This class creates a cutting statistics table in the database."""

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='instance model user')
    plotter = models.ForeignKey(Plotter, on_delete=models.CASCADE,
                                verbose_name='instance model plotter')
    template = models.ForeignKey(Template, on_delete=models.CASCADE,
                                 verbose_name='instance model template')
    label = models.ForeignKey(Label, null=True, on_delete=models.SET_NULL,
                              verbose_name='instance model label')
    date_cutted = models.DateTimeField(verbose_name='Data of creation cut',
                                       default=now)

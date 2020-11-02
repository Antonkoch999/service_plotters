"""This module creates statistics table in database."""

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.materials.models import Template
from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate


class StatisticsPlotter(DateTimeDateUpdate):
    """This class creates a plotter statistics table in the database."""

    plotter = models.ForeignKey(Plotter, on_delete=models.CASCADE,
                                verbose_name=_('Plotter serial number'))
    ip = models.CharField(max_length=150, verbose_name=_('IP address plotter'))
    last_request = models.DateField(
        verbose_name=_('Last connection to server'), default=now)
    count_cut = models.IntegerField()


class StatisticsTemplate(DateTimeDateUpdate):
    """This class creates a template statistics table in the database."""

    plotter = models.ForeignKey(Plotter, on_delete=models.CASCADE,
                                verbose_name=_('Plotter serial number'))
    template = models.ForeignKey(Template, on_delete=models.CASCADE,
                                 verbose_name=_('Name of template'))
    count = models.IntegerField()


class CuttingTransaction(DateTimeDateUpdate):
    """This class creates a cutting statistics table in the database."""

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name=_('User'))
    plotter = models.ForeignKey(Plotter, on_delete=models.CASCADE,
                                verbose_name=_('Plotter serial number'))
    template = models.ForeignKey(Template, on_delete=models.CASCADE,
                                 verbose_name=_('Name of template'))
    # label = models.ForeignKey(Label, null=True, on_delete=models.SET_NULL,
    #                           verbose_name='instance model label')
    date_cutted = models.DateTimeField(verbose_name=_('Data of creation cut'),
                                       default=now)

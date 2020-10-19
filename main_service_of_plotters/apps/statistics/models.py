from django.db import models

from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.materials.models import Template


class StatisticsPlotter(models.Model):
    """This class creates a plotter statistics table in the database."""

    IP = models.CharField(max_length=150, verbose_name='IP address plotter')
    last_request = models.DateField(verbose_name='last connection to server')
    count_cut = models.IntegerField()


class StatisticsTemplate(models.Model):
    """This class creates a template statistics table in the database."""

    plotter_id = models.ForeignKey(Plotter, on_delete=models.CASCADE,
                                   verbose_name='instance model plotter')
    template_id = models.ForeignKey(Template, on_delete=models.CASCADE,
                                    verbose_name='instance model template')
    count = models.IntegerField()

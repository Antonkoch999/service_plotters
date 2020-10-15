from django.db import models
from main_service_of_plotters.materials.models import Template
from main_service_of_plotters.device.models import Plotter
# Create your models here.


class StatisticsPlotter(models.Model):
    IP = models.CharField(max_length=150)
    last_request = models.DateField()
    count_cut = models.IntegerField()


class StatisticsTemplate(models.Model):
    plotter_id = models.ForeignKey(Plotter, on_delete=models.CASCADE)
    template_id = models.ForeignKey(Template, on_delete=models.CASCADE)
    count = models.IntegerField()

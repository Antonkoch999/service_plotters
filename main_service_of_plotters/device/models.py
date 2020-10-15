from django.db import models
from main_service_of_plotters.users.models import User


class Plotter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    serial_number = models.IntegerField()



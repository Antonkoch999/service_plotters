from django.db import models


class Template(models.Model):
    category = models.CharField(max_length=60, blank=True)
    date_creation = models.DateField()
    name = models.CharField(max_length=100, blank=True)


class Label(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    scratch_code = models.CharField(max_length=250, unique=True, blank=True)
    barcode = models.CharField(max_length=250, unique=True, blank=True)
    date_creation = models.DateField()
    date_life = models.DateField()
    count = models.IntegerField()
    lot = models.IntegerField()
    size = models.CharField(max_length=150, blank=True)

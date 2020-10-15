from django.db import models


class Template(models.Model):
    """This class creates template table."""

    category = models.CharField(max_length=60, blank=True,
                                verbose_name='category template')
    date_creation = models.DateField(verbose_name='date of creation template')
    name = models.CharField(max_length=100, blank=True,
                            verbose_name='name of template')


class Label(models.Model):
    """This class creates label table."""

    template = models.ForeignKey(Template, on_delete=models.CASCADE,
                                 verbose_name='instance model template')
    scratch_code = models.CharField(max_length=250, unique=True, blank=True,
                                    verbose_name='Unique scratch code')
    barcode = models.CharField(max_length=250, unique=True, blank=True,
                               verbose_name='Unique barcode')
    date_creation = models.DateField(verbose_name='Data of creation label')
    date_life = models.DateField(verbose_name='Lifetime of label')
    count = models.IntegerField()
    lot = models.IntegerField()
    size = models.CharField(max_length=150, blank=True,
                            verbose_name='Size of label')

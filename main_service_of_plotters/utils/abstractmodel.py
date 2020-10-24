from django.db import models
from django.utils.timezone import now


class DateTimeDateUpdate(models.Model):
    date_creation = models.DateTimeField(verbose_name='Data of creation',
                                         default=now)
    date_update = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        abstract = True

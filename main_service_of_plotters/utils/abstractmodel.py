from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class DateTimeDateUpdate(models.Model):
    date_creation = models.DateTimeField(verbose_name=_('Data of creation'),
                                         default=now)
    date_update = models.DateTimeField(null=True, auto_now=True, verbose_name=_('Date of update'))

    class Meta:
        abstract = True

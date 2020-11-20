"""This module creates statistics table in database."""

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.materials.models import Template
from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate


class StatisticsPlotter(DateTimeDateUpdate):
    """This class creates a plotter statistics table in the database."""

    plotter = models.ForeignKey(Plotter, on_delete=models.CASCADE,
                                verbose_name=_('Plotter serial number'))
    ip = models.GenericIPAddressField(verbose_name=_('IP'),
                                      help_text=_('IP address plotter'))
    last_request = models.DateField(
        verbose_name=_('Last connection'), default=now,
        help_text=_('Last connection to server'))
    count_cut = models.IntegerField(verbose_name=_('Count cut'),
                                    help_text=_('Count cut on plotter'))

    class Meta:
        """Metadata of StatisticsPlotter."""

        verbose_name = _("Plotter statistic")
        verbose_name_plural = _("Plotter statistics")

    @staticmethod
    def add_to_statistics_or_create(plotter, ip):
        """Find object statistics plotter and adding count_cut.

        Search statistics plotter with plotter and IP.
        If founded updates count_cut, if not create new one.
        """
        qs = StatisticsPlotter.objects.filter(plotter=plotter, ip=ip)
        if not qs.exists():
            StatisticsPlotter.objects.create(
                plotter=plotter,
                ip=ip,
                count_cut=1
            )
        else:
            statistic_inst = qs.first()
            statistic_inst.count_cut += 1
            statistic_inst.save()


class StatisticsTemplate(DateTimeDateUpdate):
    """This class creates a template statistics table in the database."""

    plotter = models.ForeignKey(Plotter, on_delete=models.CASCADE,
                                verbose_name=_('Plotter serial number'))
    template = models.ForeignKey(Template, on_delete=models.CASCADE,
                                 verbose_name=_('Name of template'))
    count = models.IntegerField(verbose_name=_("Count"),
                                help_text=_('Count cut template on plotter'))

    class Meta:
        """Metadata of StatisticsTemplate."""

        verbose_name = _("Template Statistic")
        verbose_name_plural = _("Template Statistics")

    @staticmethod
    def add_to_statistics_or_create(plotter, template):
        """Find object statistics template and adding count_cut.

        Search statistics template with plotter and IP.
        If founded updates count_cut, if not create new one.
        """
        qs = StatisticsTemplate.objects.filter(plotter=plotter,
                                               template=template)
        if not qs.exists():
            StatisticsTemplate.objects.create(
                plotter=plotter,
                template=template,
                count=1
            )
        else:
            statistic_inst = qs.first()
            statistic_inst.count += 1
            statistic_inst.save()


class CuttingTransaction(DateTimeDateUpdate):
    """This class creates a cutting statistics table in the database."""

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name=_('User'))
    plotter = models.ForeignKey(Plotter, on_delete=models.CASCADE,
                                verbose_name=_('Plotter'))
    template = models.ForeignKey(Template, on_delete=models.CASCADE,
                                 verbose_name=_('Name of template'))

    class Meta:
        """Metadata of CuttingTransaction."""

        verbose_name = _("Cutting Transaction")
        verbose_name_plural = _("Cutting Transactions")

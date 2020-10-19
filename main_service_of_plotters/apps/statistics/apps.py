from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StatisticsAppConfig(AppConfig):
    name = "main_service_of_plotters.apps.statistics"
    verbose_name = _("Statistics")

"""This class helps to include application configuration in settings."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StatisticsAppConfig(AppConfig):
    """Class representing a Statistics application and its configuration."""

    name = "main_service_of_plotters.apps.statistics"
    verbose_name = _("Statistics")

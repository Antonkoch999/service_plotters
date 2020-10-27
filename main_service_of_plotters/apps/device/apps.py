"""This class helps to include application configuration in settings."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DeviceConfig(AppConfig):
    """Class representing a Device application and its configuration."""

    name = "main_service_of_plotters.apps.device"
    verbose_name = _("Device")

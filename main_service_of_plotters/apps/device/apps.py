from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DeviceConfig(AppConfig):
    name = "main_service_of_plotters.apps.device"
    verbose_name = _("Device")

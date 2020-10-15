from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
# class DeviceConfig(AppConfig):
#     name = 'device'


class DeviceConfig(AppConfig):
    name = "main_service_of_plotters.device"
    verbose_name = _("Device")

    def ready(self):
        try:
            import main_service_of_plotters.users.signals  # noqa F401
        except ImportError:
            pass

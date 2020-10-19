from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# class StatisticsAppConfig(AppConfig):
#     name = 'statistics'


class StatisticsAppConfig(AppConfig):
    name = "main_service_of_plotters.apps.statistics"
    verbose_name = _("Statistics")

    def ready(self):
        try:
            import main_service_of_plotters.apps.statistics.signals  # noqa F401
        except ImportError:
            pass

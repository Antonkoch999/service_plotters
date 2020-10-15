from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# class StatisticsAppConfig(AppConfig):
#     name = 'statistics_app'


class StatisticsAppConfig(AppConfig):
    name = "main_service_of_plotters.statistics_app"
    verbose_name = _("Statistics")

    def ready(self):
        try:
            import main_service_of_plotters.statistics_app.signals  # noqa F401
        except ImportError:
            pass

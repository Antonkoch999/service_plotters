from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# class MaterialsConfig(AppConfig):
#     name = 'materials'


class MaterialsConfig(AppConfig):
    name = "main_service_of_plotters.materials"
    verbose_name = _("Material")

    def ready(self):
        try:
            import main_service_of_plotters.users.signals  # noqa F401
        except ImportError:
            pass

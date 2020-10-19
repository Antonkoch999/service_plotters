from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# class MaterialsConfig(AppConfig):
#     name = 'materials'


class MaterialsConfig(AppConfig):
    name = "main_service_of_plotters.apps.materials"
    verbose_name = _("Material")

    def ready(self):
        try:
            from main_service_of_plotters import apps
        except ImportError:
            pass

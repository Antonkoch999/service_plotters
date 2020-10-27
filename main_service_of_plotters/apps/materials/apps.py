"""This class helps to include application configuration in settings."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MaterialsConfig(AppConfig):
    """Class representing a Materials application and its configuration."""

    name = "main_service_of_plotters.apps.materials"
    verbose_name = _("Material")

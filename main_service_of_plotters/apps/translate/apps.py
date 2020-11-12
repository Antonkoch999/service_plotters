"""This class helps to include application configuration in settings."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TranslateConfig(AppConfig):
    """Class representing a User application and its configuration."""

    name = "main_service_of_plotters.apps.translate"
    verbose_name = _("Translate")

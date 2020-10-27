"""This class helps to include application configuration in settings."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CategoryConfig(AppConfig):
    """Class representing a category application and its configuration."""

    name = "main_service_of_plotters.apps.category"
    verbose_name = _("Category template")

"""This class helps to include application configuration in settings."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TicketConfig(AppConfig):
    """Class representing a Ticket application and its configuration."""

    name = 'main_service_of_plotters.apps.ticket'
    verbose_name = _("Tickets")

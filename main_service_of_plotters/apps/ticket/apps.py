from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TicketConfig(AppConfig):

    name = 'main_service_of_plotters.apps.ticket'
    verbose_name = _("Tickets")

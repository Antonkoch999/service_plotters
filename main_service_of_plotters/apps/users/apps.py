"""This class helps to include application configuration in settings."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    """Class representing a User application and its configuration."""

    name = "main_service_of_plotters.apps.users"
    verbose_name = _("Users")

    def ready(self):
        """At startup application imports signals."""

        # FIXME Uncomment when import is used
        import main_service_of_plotters.apps.users.signals

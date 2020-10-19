from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "main_service_of_plotters.apps.users"
    verbose_name = _("Users")

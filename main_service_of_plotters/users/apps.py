from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# class UsersConfig(AppConfig):
#     name = 'users'

class UsersConfig(AppConfig):
    name = "main_service_of_plotters.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import main_service_of_plotters.users.signals  # noqa F401
        except ImportError:
            pass

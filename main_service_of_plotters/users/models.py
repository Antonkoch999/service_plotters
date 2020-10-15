from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.auth.models import AbstractUser
from main_service_of_plotters.users.constants import ROLE
# Create your models here.


class User(AbstractUser):
    """Default user for Main service of plotters."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    ROLE_USER = ((ROLE[key], key) for key in ROLE.keys())
    role = models.CharField(max_length=30,
                            choices=ROLE_USER, blank=True, null=True)
    dealer_id = models.IntegerField()

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

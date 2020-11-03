"""This module create table in database."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from main_service_of_plotters.apps.users.constants import ROLE


class User(AbstractUser):
    """Default user for Main service of plotters."""

    ROLE_USER = ((ROLE[key], key) for key in ROLE.keys())
    role = models.CharField(max_length=30, choices=ROLE_USER, blank=True,
                            null=True, default='User',
                            verbose_name=_('User role'))
    dealer_id = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def is_user(self):
        return self.groups.filter(name='User').exists()

    def is_dealer(self):
        return self.groups.filter(name='Dealer').exists()

    def is_administrator(self):
        return self.groups.filter(name='Administrator').exists()

    def get_absolute_url(self) -> str:
        """"Get url for user's detail view.

        :return: URL for user detail.
        """
        return reverse("api:user-detail", kwargs={"pk": self.pk})

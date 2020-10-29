"""This module create table in database."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from main_service_of_plotters.apps.users.constants import ROLE


class User(AbstractUser):
    """Default user for Main service of plotters."""

    ROLE_USER = ((ROLE[key], key) for key in ROLE.keys())
    role = models.CharField(max_length=30, choices=ROLE_USER, blank=True,
                            null=True, default='User',
                            verbose_name='User role')
    dealer_id = models.CharField(max_length=30, blank=True, null=True)

    def is_user(self):
        return self.role == ROLE['User']

    def is_dealer(self):
        return self.role == ROLE['Dealer']

    def is_administrator(self):
        return self.role == ROLE['Administrator']

    def get_absolute_url(self) -> str:
        """"Get url for user's detail view.

        :return: URL for user detail.
        """
        return reverse("users:detail", kwargs={"username": self.username})

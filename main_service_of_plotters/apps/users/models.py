"""This module create table in database."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from main_service_of_plotters.apps.users.constants import ROLE


class User(AbstractUser):
    """Default user for Main service of plotters."""

    ROLE_USER = tuple(ROLE.items())
    role = models.CharField(
        max_length=30, choices=ROLE_USER,
        blank=True, null=True,
        verbose_name=_('User role'),
        help_text=_('User\'s role defines all allowed actions and permissions of the user in system.')
    )
    dealer = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_('Dealer'),
        related_name='attached_users',
        help_text=_('Dealer who suplies user with stuff. Only for `User` role only.')
    )

    class Meta:
        """Metadata for user model."""

        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def is_user(self) -> bool:
        """Return True, if user belong to `User` caste."""
        return self.groups.filter(name='User').exists()

    def is_dealer(self) -> bool:
        """Return True, if user belong to `Dealer` caste."""
        return self.groups.filter(name='Dealer').exists()

    def is_administrator(self) -> bool:
        """Return True, if user belong to `Administrator` caste."""
        return self.groups.filter(name='Administrator').exists()

    def is_technical_specialist(self) -> bool:
        """Return True, if user belong to `Technical Specialist` caste."""
        return self.groups.filter(name=ROLE['Technical_Specialist']).exists()

    def get_absolute_url(self) -> str:
        """"Get url for user's detail view.

        :return: URL for user detail.
        """
        return reverse("api:user-detail", kwargs={"pk": self.pk})

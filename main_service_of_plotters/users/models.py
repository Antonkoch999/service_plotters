from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractUser
from main_service_of_plotters.users.constants import ROLE


class User(AbstractUser):
    """Default user for Main service of plotters."""

    ROLE_USER = ((ROLE[key], key) for key in ROLE.keys())
    role = models.CharField(max_length=30, choices=ROLE_USER, blank=True,
                            null=True, default='User',
                            verbose_name='User role')
    dealer_id = models.CharField(max_length=30, blank=True, null=True)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"username": self.username})

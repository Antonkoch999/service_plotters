"""Models for work with tickets here."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate
from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.apps.device.models import Plotter
from .constants import StatusVariants

class Ticket(DateTimeDateUpdate):
    """Request for a technical support with description of the problem."""
    header = models.CharField(
        verbose_name=_("Header"),
        max_length=50,
        blank=False,
        help_text=_("Short description of problem.")
    )
    text = models.TextField(
        verbose_name=_("Text"),
        help_text=_("Description of problem"),
        blank=True
    )
    media_file = models.FileField(
        verbose_name=_('Attached media file'),
        upload_to='ticket_media/',
        null=True
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=1,
        blank=False,
        choices=StatusVariants,
        default=StatusVariants.OPEN
    )
    reporter = models.ForeignKey(
        verbose_name=_("Repoeter"),
        to=User,
        limit_choices_to={'is_user': True},
        on_delete=models.CASCADE,
        releated_name='created_tickets',
        help_text=_("User who create ticket"),
        null=False,
        blank=False
    )
    plotter = models.ForeignKey(
        verbose_name=_("Plotter"),
        to=Plotter,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    assignee = models.ForeignKey(
        verbose_name=_("Assignee"),
        to=User,
        limit_choices_to={'is_technical_specialist': True},
        on_delete=models.SET_NULL,
        releated_name='managed_tickets',
        null=True,
        default=None,
        help_text=_('Technical Specialist who manage ticket')
    )

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")


# class PopularProblem(models.Model):
#     name = models.CharField(
#         verbose_name=_("Name"),
#         max_length=100,
#         help_text=_("Short name of ")
    # )

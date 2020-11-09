"""Models for work with tickets here."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from main_service_of_plotters.utils.abstractmodel import DateTimeDateUpdate
from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.apps.users.constants import ROLE
from main_service_of_plotters.apps.device.models import Plotter
from .constants import StatusVariants


HEADER_MAX_LENGTH = 50


class Ticket(DateTimeDateUpdate):
    """Request for a technical support with description of the problem."""

    status_variants = StatusVariants

    header = models.CharField(
        verbose_name=_("Header"),
        max_length=HEADER_MAX_LENGTH,
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
        null=True,
        blank=True
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=1,
        blank=False,
        choices=StatusVariants.choices,
        default=StatusVariants.OPEN
    )
    reporter = models.ForeignKey(
        verbose_name=_("Reporter"),
        to=User,
        limit_choices_to={'role': ROLE["User"]},
        on_delete=models.CASCADE,
        related_name='created_tickets',
        help_text=_("User who create ticket"),
        null=False,
        blank=False
    )
    plotters = models.ManyToManyField(
        verbose_name=_("Plotters"),
        to=Plotter,
        related_name="tickets",
        blank=False
    )
    assignee = models.ForeignKey(
        verbose_name=_("Assignee"),
        to=User,
        limit_choices_to={'role': ROLE["Technical_Specialist"]},
        on_delete=models.SET_NULL,
        related_name='managed_tickets',
        null=True,
        blank=True,
        help_text=_('Technical Specialist who manage ticket')
    )
    answer = models.TextField(
        verbose_name=_("Answer"),
        blank=True,
        help_text=_("Answer of assigned technical specialist")
    )
    answer_attached_file = models.FileField(
        verbose_name=_('Answer media file'),
        upload_to='ticket_media/',
        null=True,
        blank=True,
        help_text=_("Media file attached by assigned technical specialist")
    )

    class Meta:

        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        permissions = [
            ("can_report_problem", "Can report a problem"),
            ("can_close_ticket", "Can change ticket status to Close")
        ]

    def __str__(self):
        """
        Return string representation of ticket
        """
        return f"{_('Ticket')} #{self.pk}: \"{self.header}\""


class PopularProblem(models.Model):
    """Model descride list with popular problems."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
        help_text=_("Short name of problem, will be displayed"),
        blank=False
    )
    populated_header = models.CharField(
        verbose_name=_("Populated Header"),
        max_length=HEADER_MAX_LENGTH,
        blank=False,
        help_text=_("Text what will be populated in created ticket header")
    )
    populated_text = models.TextField(
        verbose_name=_("Populated Text"),
        help_text=_("Text what will be populated in created ticket text"),
        blank=True
    )

    class Meta:

        verbose_name = _('Popular problem')
        verbose_name_plural = _('Popular problems')

    def __str__(self):
        """
        Return string representation of popular problem
        """
        return f"{_('Popular problem')} \"{self.name}\""

"""List of constants of `Ticket` models."""

from django.utils.translation import gettext_lazy as _

from django.db import models


class StatusVariants(models.TextChoices):
    """Enumeration of statuses.

    Available: OPEN, IN_WORK, SOLVED, CLOSED.
    """

    OPEN = 'O', _('Open')
    IN_WORK = 'W', _('In Work')
    SOLVED = 'S', _('Solved')
    CLOSED = 'C', _('Closed')


# length of header of ticket in model
HEADER_MAX_LENGTH = 50

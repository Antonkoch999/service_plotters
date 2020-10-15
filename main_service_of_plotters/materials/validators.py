from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def validate_scratch_code(value):
    if not value.isdigit():
        raise ValidationError(
            gettext_lazy(f'{value} is not number')
        )
    if not int(value) == 16:
        raise ValidationError(
            gettext_lazy(f'{value} is not 16 characters')
        )


def validate_barcode(value):
    if not value.isdigit():
        raise ValidationError(
            gettext_lazy(f'{value} is not number')
        )
    if not int(value) == 16:
        raise ValidationError(
            gettext_lazy(f'{value} is not 16 characters')
        )


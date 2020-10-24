import os

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def validate_unique_code(value):
    if not value.isdigit():
        raise ValidationError(
            gettext_lazy(f'{value} is not number')
        )
    if not len(value) == 16:
        raise ValidationError(
            gettext_lazy(f'{value} is not 16 characters')
        )


def validate_file_plt(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.plt', ]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_file_photo(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.png', '.svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

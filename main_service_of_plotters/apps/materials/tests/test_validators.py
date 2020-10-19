from django.test import TestCase
from django.core.exceptions import ValidationError
from main_service_of_plotters.apps.materials.validators import validate_unique_code


class TestValidator(TestCase):

    def test_validate_count_number(self):
        with self.assertRaises(ValidationError) as context:
            validate_unique_code('111122223333444')

        self.assertTrue('111122223333444 is not 16 characters' in context.exception)

    def test_validate_unique_code(self):
        with self.assertRaises(ValidationError) as context:
            validate_unique_code('111122223333aa444')

        self.assertTrue(
            '111122223333aa444 is not number' in context.exception)


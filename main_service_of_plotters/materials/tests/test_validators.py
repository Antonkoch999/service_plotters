from django.test import TestCase
from django.core.exceptions import ValidationError
from main_service_of_plotters.materials.validators import validate_barcode,\
    validate_scratch_code


# class TestValidator(TestCase):
#
#     def test_valedate_barcode(self):
#         result = validate_barcode('111122223333444')
#         self.assertRaises()

class TestValidator(TestCase):

    def test_valedate_barcode_count_characters(self):
        with self.assertRaises(ValidationError) as context:
            validate_barcode('111122223333444')

        self.assertTrue('111122223333444 is not 16 characters' in context.exception)

    def test_valedate_barcode_characters(self):
        with self.assertRaises(ValidationError) as context:
            validate_barcode('111122223333aa444')

        self.assertTrue(
            '111122223333aa444 is not number' in context.exception)

    def test_validate_scratch_code_count_characters(self):
        with self.assertRaises(ValidationError) as context:
            validate_scratch_code('111122223333444')

        self.assertTrue('111122223333444 is not 16 characters' in context.exception)

    def test_valedate_scratch_code_characters(self):
        with self.assertRaises(ValidationError) as context:
            validate_scratch_code('111122223333aa444')

        self.assertTrue(
            '111122223333aa444 is not number' in context.exception)

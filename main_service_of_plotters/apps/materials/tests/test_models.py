from datetime import timedelta

from django.test import TestCase
from django.utils.timezone import now

from main_service_of_plotters.apps.materials.models import Template, Label
from main_service_of_plotters.apps.category.models import (DeviceCategory,
                                                           Manufacturer,
                                                           ModelsTemplate)
from main_service_of_plotters.apps.device.tests.test_admin import create_user


class MaterialsCreateTest(TestCase):

    def setUp(self):
        user = create_user()
        self.user = user['User']
        self.dealer = user['Dealer']

        self.device = DeviceCategory.objects.create(name="Device")
        self.manufacturer = Manufacturer.objects.create(
            device_category=DeviceCategory.objects.get(name='Device'),
            name="Manufacturer")
        self.modelstemplate = ModelsTemplate.objects.create(
            manufacturer=Manufacturer.objects.get(name="Manufacturer"),
            name="Modelstemplate")
        self.template = Template.objects.create(
            device_category=self.device,
            manufacturer_category=self.manufacturer,
            model_category=self.modelstemplate,
            name="Template",
            file_photo=".main_service_of_plotters/static/test/test_image.png",
            file_plt=".main_service_of_plotters/static/test/test_file.plt",
        )
        self.label = Label.objects.create(
            scratch_code='0000000000000000',
            barcode='0000000000000000',
            count=10,
            dealer=self.dealer,
            user=self.user,
            is_active=False,
        )
        self.test_template = Template.objects.get(name="Template")
        self.test_label = Label.objects.get(scratch_code='0000000000000000')

    def test_create_template(self):
        self.assertEqual(self.test_template.name, "Template")
        self.assertEqual(self.test_template.device_category.name, "Device")

    def test_template_str(self):
        self.assertEqual(str(self.template), f'Template {self.template.name}')

    def test_create_label(self):
        self.assertEqual(self.test_label.scratch_code, '0000000000000000')

    def test_label_str(self):
        self.assertEqual(str(self.label),
                         f'Scratch code {self.label.scratch_code}')

    def test_is_active_and_not_expired_after_activation(self):
        self.label.is_active = True
        self.label.date_of_activation = now()
        self.assertEqual(self.label.is_active_and_not_expired, True)

    def test_is_active_and_not_expired_false_for_old(self):
        self.label.is_active = True
        self.label.date_of_activation = now() - timedelta(days=10000)
        self.assertEqual(self.label.is_active_and_not_expired, False)

    def test_is_active_and_not_expired_false_for_unactive(self):
        self.label.date_of_activation = now() - timedelta(minutes=5)
        self.label.is_active = False
        self.assertEqual(self.label.is_active_and_not_expired, False)

    def test_in_terms_of_expiration_5_mins_ago(self):
        self.label.date_of_activation = now() - timedelta(minutes=5)
        self.assertEqual(self.label.is_in_terms_of_expiration, True)

    def test_in_terms_of_expiration_false_for_too_old(self):
        self.label.date_of_activation = now() - timedelta(days=10000)
        self.assertGreater(now(), self.label.date_of_expiration())
        self.assertEqual(self.label.is_in_terms_of_expiration, False)

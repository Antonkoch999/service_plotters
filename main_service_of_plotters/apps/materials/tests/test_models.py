from django.test import TestCase

from main_service_of_plotters.apps.materials.models import Template, Label
from main_service_of_plotters.apps.category.models import (DeviceCategory,
                                                           Manufacturer,
                                                           ModelsTemplate)
from main_service_of_plotters.apps.users.models import User


class MaterialsCreateTest(TestCase):

    def setUp(self):
        self.dealer = User.objects.create(
            username='Dealer',
            email='dealer',
            password='dealer',
            role='Dealer',
        )
        self.user = User.objects.create(
            username='User',
            email='user',
            password='user',
            role='User',
        )
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

    def test_create_template(self):
        self.test = Template.objects.get(name="Template")
        self.assertEqual(self.test.name, "Template")
        self.assertEqual(self.test.device_category.name, "Device")

    def test_template_str(self):
        self.assertEqual(str(self.template), f'Template {self.template.name}')

    def test_create_label(self):
        self.test = Label.objects.get(scratch_code='0000000000000000')
        self.assertEqual(self.test.scratch_code, '0000000000000000')

    def test_label_str(self):
        self.assertEqual(str(self.label),
                         f'Scratch code {self.label.scratch_code}')

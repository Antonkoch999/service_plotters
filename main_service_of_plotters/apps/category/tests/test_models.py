from django.test import TestCase
from ..models import DeviceCategory, Manufacturer, ModelsTemplate


class CategoryCreateModelsTest(TestCase):

    def setUp(self):
        self.device = DeviceCategory.objects.create(name="Test")
        self.manufacturer = Manufacturer.objects.create(
            device_category=DeviceCategory.objects.get(name='Test'),
            name="Test")
        self.modelstemplate = ModelsTemplate.objects.create(
            manufacturer=Manufacturer.objects.get(name="Test"),
            name="Test")

    def test_device_category(self):
        test = DeviceCategory.objects.get(name="Test")
        self.assertEqual(test.name, "Test")

    def test_manufacturer(self):
        test = Manufacturer.objects.get(name="Test")
        self.assertEqual(test.device_category.name, "Test")

    def test_models_template(self):
        test = ModelsTemplate.objects.get(name="Test")
        self.assertEqual(test.manufacturer.name, "Test")

    def test_device_category_str(self):
        self.assertEqual(str(self.device), f'Category {self.device.name}')

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer),
                         f'Category {self.manufacturer.device_category.name}'
                         f' | Manufacturer {self.manufacturer.name}')

    def test_models_template_str(self):
        self.assertEqual(
            str(self.modelstemplate),
            f'Category {self.modelstemplate.manufacturer.device_category.name}'
            f' | Manufacturer {self.modelstemplate.manufacturer.name} |'
            f' Model {self.modelstemplate.name}')

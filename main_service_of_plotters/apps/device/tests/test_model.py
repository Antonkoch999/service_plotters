from django.test import TestCase

from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.users.models import User


class TestModelPlotter(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username='admin',
                                                  email='admin@admin.com',
                                                  password='xx')
        self.user.save()
        self.plotter = Plotter(user=self.user, serial_number=1111222233334444)
        self.plotter.save()

    def test_model_plotter(self):
        self.assertEqual(self.user.username, 'admin')
        self.assertEqual(self.plotter.serial_number, 1111222233334444)

    def test_model_plotter_count_number(self):
        self.assertEqual(len(str(self.plotter.serial_number)), 16)

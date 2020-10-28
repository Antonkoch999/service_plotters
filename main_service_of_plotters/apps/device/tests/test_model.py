from django.test import TestCase, Client

from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.users.models import User
from ...users.constants import ROLE


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

    def test_model_plotter_str(self):
        self.assertEqual(str(self.plotter), 'Plotter 1111222233334444')


class TestAdminPlotter(TestCase):
    """Testing plotter admin page."""

    def setUp(self):
        """"Setting up environment."""
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='admin'
        )
        self.user1 = User.objects.create(
            username='user1',
            password='user1'
        )
        self.user2 = User.objects.create(
            username='user2',
            password='user2'
        )
        self.admin = User.objects.create(
            username='admin',
            password='admin',
            role=ROLE['Administrator']
        )
        self.dealer1 = User.objects.create(
            username='dealer',
            password='dealer'
            role=ROLE['Dealer']
        )
        self.plotter1 = Plotter(user=None, dealer=None, serial_number=1)
        self.c = Client()



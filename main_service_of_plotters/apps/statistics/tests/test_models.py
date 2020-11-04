from django.test import TestCase

from main_service_of_plotters.apps.statistics.models import (
    StatisticsPlotter, StatisticsTemplate, CuttingTransaction)
from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.users.models import User


class StatisticsCreateTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='admin',
                                                  email='admin@admin.com',
                                                  password='xx')
        self.user.save()
        self.plotter = Plotter(
            user=self.user,
            serial_number=1111222233334444)
        self.plotter.save()

        self.statistics_plotter = StatisticsPlotter.objects.create(
            plotter=self.plotter,
            ip='132.144.21.31',
            last_request='2019-08-25',
            count_cut=30,
        )

    def test_create_statistics_plotter(self):
        self.test = StatisticsPlotter.objects.get(ip='132.144.21.31',)
        self.assertEqual(self.test.ip, '132.144.21.31')
        self.assertEqual(self.test.plotter.serial_number, 1111222233334444)



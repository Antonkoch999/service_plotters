from datetime import timedelta, datetime

from django.test import TestCase, Client
from django.http import HttpRequest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Group
from django.utils.timezone import now

from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.apps.materials.models import Label
from ...users.constants import ROLE
from ..admin import PlotterAdmin


class TestModelPlotter(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username='admin',
                                                  email='admin@admin.com',
                                                  password='xx')
        self.user.save()
        self.plotter = Plotter(user=self.user, serial_number=1111222233334444)
        self.plotter.save()
        self.label1 = Label()

    def test_model_plotter(self):
        self.assertEqual(self.user.username, 'admin')
        self.assertEqual(self.plotter.serial_number, 1111222233334444)

    def test_model_plotter_count_number(self):
        self.assertEqual(len(str(self.plotter.serial_number)), 16)

    def test_model_plotter_str(self):
        self.assertEqual(str(self.plotter), 'Plotter 1111222233334444')

    def test_link_label(self):
        self.assertEqual(self.plotter.linked_labels.count(), 0)
        self.plotter.link_label(self.label1)
        self.assertEqual(self.plotter.linked_labels.count(), 1)
        self.assertIn(self.label1, self.plotter.linked_labels.all())

    def test_first_linked_label(self):
        # Label without available count no returning
        label_no_count = Label(barcode='1111111111111111',
                               scratch_code='2111111111111111')
        self.plotter.link_label(label_no_count)
        label_no_count.available_count = 0
        label_no_count.save()

        # not active label dont returning
        label_not_active = Label(barcode='1111111111111112',
                                 scratch_code='2111111111111112',
                                 count=50)
        self.plotter.link_label(label_not_active)
        label_not_active.is_active = False
        label_not_active.save()

        # expired label dont returning
        label_expired = Label(barcode='1111111111111113',
                              scratch_code='2111111111111113',
                              count=50)
        self.plotter.link_label(label_expired)
        label_expired.date_of_activation = datetime(1980, 1, 1, 1, 0, 0)
        label_expired.save()

        label_second = Label(barcode='1111111111111115',
                             scratch_code='2111111111111115',
                             count=50)
        self.plotter.link_label(label_second)

        label_first = Label(barcode='1111111111111114',
                            scratch_code='2111111111111114',
                            count=50)
        self.plotter.link_label(label_first)
        label_first.date_of_activation = now() - timedelta(days=5)
        label_first.save()

        first_returned = self.plotter.first_linked_label
        self.assertNotEqual(first_returned, label_no_count,
                            f"Label with {label_no_count.available_count} available counts returned as first")
        self.assertNotEqual(first_returned, label_not_active,
                            f"Label with is_active = {label_not_active.is_active} returned as first")
        self.assertNotEqual(first_returned, label_expired,
                            f"Expired label f{first_returned.date_of_expiration} returned, but now {now()}")
        self.assertNotEqual(first_returned, label_second,
                            f"Second label retruned but must be first. {first_returned.date_of_activation}"
                            f" must be older then {label_first.date_of_activation}")

        self.assertEqual(first_returned, label_first)

    def test_available_film(self):
        # not active label not countin
        label_not_active = Label(barcode='1111111111111112',
                                 scratch_code='2111111111111112',
                                 count=1)
        self.plotter.link_label(label_not_active)
        label_not_active.is_active = False
        label_not_active.save()

        # expired label not countin
        label_expired = Label(barcode='1111111111111113',
                              scratch_code='2111111111111113',
                              count=2)
        self.plotter.link_label(label_expired)
        label_expired.date_of_activation = datetime(1980, 1, 1, 1, 0, 0)
        label_expired.save()

        label_normal = Label(barcode='1111111111111118',
                             scratch_code='2111111111111118',
                             count=3)
        self.plotter.link_label(label_normal)


        label_not_linked = Label.objects.create(barcode='1111111111111114',
                                 scratch_code='2111111111111114',
                                 count=4)

        label_normal2 = Label(barcode='1111111111111115',
                             scratch_code='2111111111111115',
                             count=100)
        self.plotter.link_label(label_normal2)

        self.assertEqual(self.plotter.available_films(), 103)

from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client
from django.http import HttpRequest

from main_service_of_plotters.apps.materials.models import Template, Label
from main_service_of_plotters.apps.users.models import User
from django.contrib.auth.models import Group
from main_service_of_plotters.apps.statistics.admin import PlotterAdmin
from main_service_of_plotters.apps.statistics.models import (
    StatisticsPlotter, StatisticsTemplate, CuttingTransaction)
from main_service_of_plotters.apps.device.models import Plotter


class StatisticsAdminTest(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.client = Client()
        self.group_administrator = Group.objects.get_or_create(
            name='Administrator')[0]
        self.group_dealer = Group.objects.get_or_create(name='Dealer')[0]
        self.group_user = Group.objects.get_or_create(name='User')[0]

        self.administrator = User.objects.create(
            username='Administrator',
            email='administrator',
            password='administrator',
            role='Administrator',
        )
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

        self.administrator.groups.add(self.group_administrator)
        self.dealer.groups.add(self.group_dealer)
        self.user.groups.add(self.group_user)

        self.administrator.save()
        self.dealer.save()
        self.user.save()

        self.plotter = Plotter(user=self.user,
                               serial_number=1111222233334444)
        self.plotter.save()

        self.statistics_plotter = StatisticsPlotter.objects.create(
            plotter=self.plotter,
            ip='132.144.21.31',
            last_request='2019-08-25',
            count_cut=30,
        )
        self.request = HttpRequest()

    def test_statistics_plotter_get_form_administrator(self):
        test_admin_model = PlotterAdmin(model=StatisticsPlotter,
                                        admin_site=AdminSite())
        self.request.user = self.administrator
        self.assertEqual(
            list(test_admin_model.get_form(request=self.request).base_fields),
            ['date_creation', 'plotter', 'ip', 'last_request', 'count_cut'])

    def test_statistics_plotter_get_form_dealer_or_user(self):
        test_admin_model = PlotterAdmin(model=StatisticsPlotter,
                                        admin_site=AdminSite())
        self.request.user = self.dealer
        self.assertEqual(
            list(test_admin_model.get_form(request=self.request).base_fields),
            ['date_creation', 'plotter', 'last_request', 'count_cut'])

    def test_statistics_plotter_get_list_display_administrator(self):
        test_admin_model = PlotterAdmin(model=StatisticsPlotter,
                                        admin_site=AdminSite())
        self.request.user = self.administrator
        self.assertEqual(
            list(test_admin_model.get_list_display(request=self.request)),
            ['plotter', 'ip', 'last_request', 'count_cut', 'date_creation',
             'date_update']
        )

    def test_statistics_plotter_get_list_display_dealer_or_user(self):
        test_admin_model = PlotterAdmin(model=StatisticsPlotter,
                                        admin_site=AdminSite())
        self.request.user = self.dealer
        self.assertEqual(
            list(test_admin_model.get_list_display(request=self.request)),
            ['plotter', 'last_request', 'count_cut', 'date_creation',
             'date_update']
        )

from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client
from django.http import HttpRequest

from main_service_of_plotters.apps.materials.models import Template
from main_service_of_plotters.apps.statistics.admin import (
    PlotterAdmin, CuttingAdmin)
from main_service_of_plotters.apps.statistics.models import (
    StatisticsPlotter, CuttingTransaction)
from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.category.models import (DeviceCategory,
                                                           Manufacturer,
                                                           ModelsTemplate)
from main_service_of_plotters.apps.device.tests.test_admin import create_group, create_user


class StatisticsAdminTest(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.client = Client()
        group = create_group()
        user = create_user()

        self.administrator = user['Administrator']
        self.dealer = user['Dealer']
        self.user = user['User']
        self.administrator.groups.add(group['Administrator'])
        self.dealer.groups.add(group['Dealer'])
        self.user.groups.add(group['User'])

        self.administrator.save()
        self.dealer.save()
        self.user.save()

        self.device = DeviceCategory.objects.create(name="Device")
        self.manufacturer = Manufacturer.objects.create(
            device_category=DeviceCategory.objects.get(name='Device'),
            name="Manufacturer")
        self.modelstemplate = ModelsTemplate.objects.create(
            manufacturer=Manufacturer.objects.get(name="Manufacturer"),
            name="Modelstemplate")

        self.plotter = Plotter(user=self.user,
                               serial_number=1111222233334444)
        self.plotter.save()

        self.template = Template.objects.create(
            device_category=self.device,
            manufacturer_category=self.manufacturer,
            model_category=self.modelstemplate,
            name="Template",
            file_photo=".main_service_of_plotters/static/test/test_image.png",
            file_plt=".main_service_of_plotters/static/test/test_file.plt",
        )

        self.statistics_plotter = StatisticsPlotter.objects.create(
            plotter=self.plotter,
            ip='132.144.21.31',
            last_request='2019-08-25',
            count_cut=30,
        )
        self.cuttingtransaction = CuttingTransaction.objects.create(
            user=self.user,
            plotter=self.plotter,
            template=self.template,
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
            ['plotter', 'last_request', 'count_cut', 'date_creation'])

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

    def test_statistics_template_queryset_administrator(self):
        test_admin_model = CuttingAdmin(model=CuttingTransaction,
                                        admin_site=AdminSite())
        self.request.user = self.administrator
        self.assertEqual(
            list(test_admin_model.get_queryset(request=self.request)),
            [self.cuttingtransaction])

    def test_statistics_template_queryset_dealer(self):
        test_admin_model = CuttingAdmin(model=CuttingTransaction,
                                        admin_site=AdminSite())
        self.request.user = self.dealer
        self.assertEqual(
            list(test_admin_model.get_queryset(request=self.request)),
            [])

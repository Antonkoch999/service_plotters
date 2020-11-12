from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client
from django.http import HttpRequest

from main_service_of_plotters.apps.materials.models import Template, Label
from main_service_of_plotters.apps.category.models import (DeviceCategory,
                                                           Manufacturer,
                                                           ModelsTemplate)
from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.apps.materials.admin import CustomLabelAdmin
from main_service_of_plotters.apps.device.tests.test_admin import (
    create_user, create_group)


class MaterialsAdminTest(TestCase):

    def setUp(self):
        group = create_group()
        user = create_user()
        self.site = AdminSite()
        self.client = Client()

        self.dealer1 = User.objects.create(
            username='Dealer1',
            email='dealer1',
            password='dealer1',
            role='Dealer1',
        )
        self.user1 = User.objects.create(
            username='User1',
            email='user1',
            password='user1',
            role='User1',
        )
        self.administrator = user['Administrator']
        self.dealer = user['Dealer']
        self.user = user['User']

        self.administrator.groups.add(group['Administrator'])
        self.dealer.groups.add(group['Dealer'])
        self.user.groups.add(group['User'])
        self.dealer1.groups.add(group['Dealer'])
        self.user1.groups.add(group['User'])

        self.administrator.save()
        self.dealer.save()
        self.user.save()
        self.dealer1.save()
        self.user1.save()

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

        self.request = HttpRequest()

    def test_label_action_administrator(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.administrator
        self.assertEqual(
            list(test_admin_model.get_actions(request=self.request)),
            ['add_dealer'])

    def test_label_action_dealer(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.dealer
        self.assertEqual(
            list(test_admin_model.get_actions(request=self.request)),
            ['add_user'])

    def test_label_action_user(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.user
        self.assertEqual(
            list(test_admin_model.get_actions(request=self.request)),
            [])

    def test_label_queryset_administrator(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.administrator
        self.assertEqual(
            list(test_admin_model.get_queryset(request=self.request)),
            [self.label])

    def test_label_queryset_dealer(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.dealer
        self.assertEqual(
            list(test_admin_model.get_queryset(request=self.request)),
            [self.label])

    def test_label_queryset_user(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.user
        self.assertEqual(
            list(test_admin_model.get_queryset(request=self.request)),
            [self.label])

    def test_label_queryset_dealer1(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.dealer1
        self.assertEqual(
            list(test_admin_model.get_queryset(request=self.request)),
            [])

    def test_label_queryset_user1(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.user1
        self.assertEqual(
            list(test_admin_model.get_queryset(request=self.request)),
            [])

    def test_label_get_form_administrator(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.administrator
        self.assertEqual(
            list(test_admin_model.get_form(request=self.request,
                                           obj=self.label).base_fields),
            ['scratch_code', 'barcode', 'count', 'dealer',
             'user', 'is_active']
        )

    def test_label_get_form_dealer(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.dealer
        self.assertEqual(
            list(test_admin_model.get_form(request=self.request,
                                           obj=self.label).base_fields),
            ['barcode', 'count', 'user']
        )

    def test_label_get_form_user(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.user
        print(self.request.user.groups.all())
        self.assertEqual(
            list(test_admin_model.get_form(request=self.request,
                                           obj=self.label).base_fields),
            ['barcode', 'count', 'date_of_activation', 'linked_plotter']
        )

    def test_label_get_list_display_administrator(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.administrator
        self.assertEqual(
            list(test_admin_model.get_list_display(request=self.request)),
            ['scratch_code', 'barcode', 'count', 'available_count',
             'dealer', 'user', 'date_of_expiration', 'is_active', ]
        )

    def test_label_get_list_display_dealer_or_user(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.dealer
        self.assertEqual(
            list(test_admin_model.get_list_display(request=self.request)),
            ['barcode', 'count', 'available_count',
             'dealer', 'user', 'date_of_expiration', 'days_before_expiration',
             'is_active', ]
        )

    def test_label_get_list_filter_administrator(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.administrator
        self.assertEqual(
            list(test_admin_model.get_list_filter(request=self.request)),
            ['date_creation', 'user', 'dealer']
        )

    def test_label_get_list_filter_dealer_or_user(self):
        test_admin_model = CustomLabelAdmin(model=Label,
                                            admin_site=AdminSite())
        self.request.user = self.dealer
        self.assertEqual(
            list(test_admin_model.get_list_filter(request=self.request)),
            ['date_creation']
        )

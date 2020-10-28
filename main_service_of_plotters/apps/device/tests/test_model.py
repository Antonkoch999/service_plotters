from django.test import TestCase, Client
from django.http import HttpRequest
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import Group

from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.users.models import User
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
        # Add users
        self.superuser = User.objects.create_superuser(
            username='supadmin',
            password='supadmin'
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
            password='dealer',
            role=ROLE['Dealer']
        )

        # Create groups
        self.group_administrator = Group.objects.get_or_create(
            name='Administrator')[0]
        self.group_dealer = Group.objects.get_or_create(name='Dealer')[0]
        self.group_user = Group.objects.get_or_create(name='User')[0]

        # Assign Groups
        self.admin.groups.add(self.group_administrator)
        self.dealer1.groups.add(self.group_dealer)
        self.user1.groups.add(self.group_user)
        self.user2.groups.add(self.group_user)

        # Miscs
        self.plotter1 = Plotter(user=None, dealer=None, serial_number=1)
        self.plotter1.save()
        self.plotter2 = Plotter(user=None,
                                dealer=self.dealer1, serial_number=2)
        self.plotter2.save()
        self.plotter3 = Plotter(user=self.user1,
                                dealer=self.dealer1, serial_number=3)
        self.plotter3.save()
        self.c = Client()
        self.request = HttpRequest()

    def get_model_admin_with_logged_user(self, user):
        self.request.user = user
        model_admin = PlotterAdmin(model=Plotter, admin_site=AdminSite())
        return model_admin

    def test_admin_queryset_all_plotters(self):
        model_admin = self.get_model_admin_with_logged_user(self.admin)
        qs = model_admin.get_queryset(request=self.request)
        self.assertEqual(qs.count(), Plotter.objects.all().count())

    def test_dealer_queryset_only_owned_plotters(self):
        model_admin = self.get_model_admin_with_logged_user(self.dealer1)
        qs = model_admin.get_queryset(request=self.request)
        for plotter in qs:
            self.assertEqual(plotter.dealer, self.dealer1)

    def test_user_queryset_only_owned_plotters(self):
        model_admin = self.get_model_admin_with_logged_user(self.user1)
        qs = model_admin.get_queryset(request=self.request)
        for plotter in qs:
            self.assertEqual(plotter.user, self.user1)

    def test_user_without_plotters_queryset_O_plotters(self):
        model_admin = self.get_model_admin_with_logged_user(self.user2)
        qs = model_admin.get_queryset(request=self.request)
        self.assertEqual(qs.count(), 0,
                         'User2 can see another plotters')

    def test_dealer_cannot_see_scratch_code_in_list_display(self):
        model_admin = self.get_model_admin_with_logged_user(self.dealer1)
        self.assertNotIn(
            'scratch_code',
            model_admin.get_list_display(self.request))

    def test_url_list_have_additional_url_named_add_label(self):
        model_admin = self.get_model_admin_with_logged_user(self.dealer1)
        self.assertEqual(model_admin.get_urls()[0].name, 'add_label')

    def test_account_action_return_button(self):
        model_admin = self.get_model_admin_with_logged_user(self.dealer1)
        action = model_admin.account_actions(obj=self.plotter1)
        self.assertIn('<a class="button"', action)

    def admin_have_action_button_in_list_display(self):
        model_admin = self.get_model_admin_with_logged_user(self.admin)
        self.assertIn(
            'account_action',
            model_admin.get_list_display(request=self.request)
        )

    def dealer_not_have_action_button_in_list_display(self):
        model_admin = self.get_model_admin_with_logged_user(self.dealer1)
        self.assertNotIn(
            'account_action',
            model_admin.get_list_display(request=self.request)
        )

    def user_have_action_button_in_list_display(self):
        model_admin = self.get_model_admin_with_logged_user(self.user1)
        self.assertIn(
            'account_action',
            model_admin.get_list_display(request=self.request)
        )

    # TODO test ModelAdmin from
    # TODO test custom action

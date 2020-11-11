from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client
from django.http import HttpRequest

from main_service_of_plotters.apps.ticket.models import Ticket
from main_service_of_plotters.apps.users.models import User
from django.contrib.auth.models import Group
from main_service_of_plotters.apps.ticket.admin import TicketAdmin
from main_service_of_plotters.apps.statistics.models import (
    StatisticsPlotter, StatisticsTemplate, CuttingTransaction)
from main_service_of_plotters.apps.device.models import Plotter
from main_service_of_plotters.apps.category.models import (DeviceCategory,
                                                           Manufacturer,
                                                           ModelsTemplate)


class TicketAdminTest(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.client = Client()
        self.request = HttpRequest()
        self.group_tech = Group.objects.get_or_create(
            name='Technical_Specialist')[0]
        self.tech = User.objects.create(
            username='Tech',
            email='tech',
            password='tech',
            role='Technical_Specialist',
        )
        self.tech1 = User.objects.create(
            username='Tech1',
            email='tech1',
            password='tech1',
            role='Technical_Specialist',
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
        self.tech.groups.add(self.group_tech)
        self.tech.save()
        self.tech1.groups.add(self.group_tech)
        self.tech1.save()

        self.plotter = Plotter.objects.create(
            dealer=self.dealer,
            user=self.user,
            serial_number=1111222233334444,
        )
        self.ticket = Ticket.objects.create(
            header="Test_header",
            text="Test_text",
            reporter=self.user,
            assignee=self.tech,
            answer="test_answer",
        )
        self.ticket.save()
        self.ticket.plotters.set([self.plotter])
        self.ticket.save()

        self.ticket1 = Ticket.objects.create(
            header="Test_header1",
            text="Test_text1",
            status="C",
            reporter=self.user,
            assignee=self.tech1,
            answer="test_answer1",
        )
        self.ticket1.save()
        self.ticket1.plotters.set([self.plotter])
        self.ticket1.save()

    def test_ticket_admin_get_form_tech(self):
        test_admin_model = TicketAdmin(model=Ticket,
                                        admin_site=AdminSite())
        self.request.user = self.tech
        self.assertEqual(
            list(test_admin_model.get_form(request=self.request).base_fields),
            ['header', 'text', 'media_file', 'status', 'assignee', 'answer',
             'answer_attached_file'])

    def test_ticket_admin_get_form_user(self):
        test_admin_model = TicketAdmin(model=Ticket,
                                       admin_site=AdminSite())
        self.request.user = self.user
        self.assertEqual(
            list(test_admin_model.get_form(request=self.request).base_fields),
            ['header', 'text', 'media_file', 'status', 'plotters',
             'assignee', 'answer', 'answer_attached_file'])

    def test_ticket_admin_get_list_display_tech(self):
        test_admin_model = TicketAdmin(model=Ticket,
                                       admin_site=AdminSite())
        self.request.user = self.tech
        self.assertEqual(
            list(test_admin_model.get_list_display(request=self.request)),
            ['header', 'status', 'assignee'])

    def test_ticket_admin_get_list_display_all(self):
        test_admin_model = TicketAdmin(model=Ticket,
                                       admin_site=AdminSite())
        self.request.user = self.user
        self.assertEqual(
            list(test_admin_model.get_list_display(request=self.request)),
            ['header', 'assignee', 'reporter', 'status'])

    def test_ticket_admin_get_queryset_tech(self):
        test_admin_model = TicketAdmin(model=Ticket,
                                       admin_site=AdminSite())
        self.request.user = self.tech
        self.assertEqual(
            list(test_admin_model.get_queryset(request=self.request)),
            [self.ticket])

    def test_ticket_admin_get_queryset_user(self):
        test_admin_model = TicketAdmin(model=Ticket,
                                       admin_site=AdminSite())
        self.request.user = self.user
        self.assertEqual(
            list(test_admin_model.get_queryset(request=self.request)),
            [self.ticket, self.ticket1])

    def test_ticket_admin_get_list_filter_tech(self):
        test_admin_model = TicketAdmin(model=Ticket,
                                       admin_site=AdminSite())
        self.request.user = self.tech
        self.assertEqual(
            list(test_admin_model.get_list_filter(request=self.request)),
            ['status'])

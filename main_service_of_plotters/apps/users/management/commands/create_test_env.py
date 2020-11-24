"""This module create custom command for creating users and group."""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from main_service_of_plotters.apps.users.models import User
from main_service_of_plotters.apps.users.constants import ROLE


class Command(BaseCommand):
    """Create custom command."""

    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        """Logic custom command.

        Create users and groups and appoints permissions for groups."""
        groups = {'Administrator': None, 'Dealer': None, 'User': None,
                  'Technical_Specialist': None}

        for group in groups.keys():
            groups[group] = Group.objects.get_or_create(name=group)[0]
            groups[group].save()

        users = {'User': User.objects.get_or_create(
            username='user', role=ROLE['User'], password='12345')[0],
                 'Dealer': User.objects.get_or_create(
                     username='dealer', role=ROLE['Dealer'], password='12345')[
                     0],
                 'Administrator': User.objects.get_or_create(
                     username='administrator', role=ROLE['Administrator'],
                     password='12345')[0],
                 'Technical_Specialist': User.objects.get_or_create(
                     username='tech', role=ROLE['Technical_Specialist'],
                     password='12345')[0]
                 }

        permission_administrator_list = (
            'Can add Plotter', 'Can change Plotter', 'Can delete Plotter',
            'Can view Plotter', 'Can add Template', 'Can change Template',
            'Can delete Template', 'Can view Template', 'Can add User',
            'Can change User', 'Can delete User', 'Can view User',
            'Can add Label', 'Can change Label', 'Can delete Label',
            'Can view Label', 'Can view Plotter statistic',
            'Can view Template Statistic', 'Can view Cutting Transaction',
            'Can add Device category', 'Can change Device category',
            'Can delete Device category', 'Can view Device category',
            'Can add Manufacturer', 'Can change Manufacturer',
            'Can delete Manufacturer', 'Can view Manufacturer',
            'Can add Model', 'Can change Model',
            'Can delete Model', 'Can view Model',
            'Can add Popular problem', 'Can change Popular problem',
            'Can delete Popular problem', 'Can view Popular problem',
            'Can change Ticket', 'Can delete Ticket', 'Can view Ticket',

        )

        permission_dealer_list = (
            'Can add User', 'Can change User', 'Can view User',
            'Can change Plotter', 'Can view Plotter', 'Can change Label',
            'Can view Label', 'Can view Device category',
            'Can view Manufacturer', 'Can view Model',
            'Can view Cutting Transaction', 'Can view Plotter statistic',
        )

        permission_user_list = (
            'Can view Plotter', 'Can view Plotter statistic', 'Can view Label',
            'Can view Device category', 'Can view Manufacturer',
            'Can view Model', 'Can report a problem', 'Can change Ticket',
            'Can change ticket status to Close', 'Can view Ticket',
        )
        permission_tech_list = (
            'Can view Popular problem', 'Can change Ticket', 'Can view Ticket',
            "Can solve ticket's problems",
        )
        permission_dealer = Permission.objects.filter(
            name__in=permission_dealer_list)
        permission_user = Permission.objects.filter(
            name__in=permission_user_list)
        permission_administrator = Permission.objects.filter(
            name__in=permission_administrator_list)
        permissions_tech = Permission.objects.filter(
            name__in=permission_tech_list)

        groups['Administrator'].permissions.add(*permission_administrator)
        groups['Dealer'].permissions.add(*permission_dealer)
        groups['User'].permissions.add(*permission_user)
        groups['Technical_Specialist'].permissions.add(*permissions_tech)
        groups['Administrator'].save()
        groups['User'].save()
        groups['Dealer'].save()
        groups['Technical_Specialist'].save()
        users['User'].save()
        users['Dealer'].save()
        users['Administrator'].save()
        users['Technical_Specialist'].save()

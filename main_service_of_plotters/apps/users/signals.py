"""This module contains signals."""

from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from main_service_of_plotters.apps.users.constants import ROLE
from main_service_of_plotters.apps.users.models import User


@receiver(post_save, sender=User)
def my_handler(sender, instance, created,  **kwargs):
    """Post-create user signal that adds the user to everyone group."""

    if created:
        try:
            if instance.role == ROLE['Dealer']:
                instance.is_staff = True
                group = Group.objects.get(name=ROLE['Dealer'])
                instance.save()
                instance.groups.add(group)
            elif instance.role == ROLE['User']:
                instance.is_staff = True
                group = Group.objects.get(name=ROLE['User'])
                instance.save()
                instance.groups.add(group)
            elif instance.role == 'Administrator':
                instance.is_staff = True
                group = Group.objects.get(name=ROLE['Administrator'])
                instance.save()
                instance.groups.add(group)
            elif instance.role == ROLE['Chief_Administrator']:
                instance.is_staff = True
                group = Group.objects.get(name=ROLE['Chief_Administrator'])
                instance.save()
                instance.groups.add(group)
        except Group.DoesNotExist:
            print('Group.DoesNotExist')

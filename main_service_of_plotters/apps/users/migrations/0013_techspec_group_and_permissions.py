# Generated by Django 3.0.10 on 2020-11-23 08:15

from django.db import migrations


def create_group_if_not_exist(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='Technical_Specialist')

def grant_permissions(apps, schema_editor):
    Permission = apps.get_model('auth', 'Permission')
    Group = apps.get_model('auth', 'Group')
    tech_spec_group = Group.objects.get(name='Technical_Specialist')
    user_group = Group.objects.get(name='User')
    admin_group = Group.objects.get(name='Administrator')
    ticket_perms = Permission.objects.filter(content_type__model='ticket')
    popproblems_perms = Permission.objects.filter(
        content_type__model='popularproblem')

    users_perms = [
        ticket_perms.get(codename='can_report_problem'),
        ticket_perms.get(codename='change_ticket'),
        ticket_perms.get(codename='can_close_ticket'),
        popproblems_perms.get(codename='view_popularproblem'),
    ]
    tech_specs_perms = [
        ticket_perms.get(codename='change_ticket'),
        popproblems_perms.get(codename='view_popularproblem'),
    ]
    admins_perms = [
        ticket_perms.get(codename='add_ticket'),
        ticket_perms.get(codename='change_ticket'),
        ticket_perms.get(codename='delete_ticket'),
        ticket_perms.get(codename='view_ticket'),
        popproblems_perms.get(codename='add_popularproblem'),
        popproblems_perms.get(codename='change_popularproblem'),
        popproblems_perms.get(codename='delete_popularproblem'),
        popproblems_perms.get(codename='view_popularproblem')
    ]

    user_group.permissions.add(*users_perms)
    tech_spec_group.permissions.add(*tech_specs_perms)
    admin_group.permissions.add(*admins_perms)

def do_nothing(*args, **kwargs):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20201109_1111'),
        ('ticket', '0007_auto_20201109_0916')
    ]

    operations = [
        migrations.RunPython(create_group_if_not_exist, do_nothing),
        migrations.RunPython(grant_permissions, do_nothing)
    ]

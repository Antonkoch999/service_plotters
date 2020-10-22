from django.db import migrations


def create_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    groups = {'Chief_Administrator': None, 'Administrator': None,
              'Dealer': None, 'User': None}

    for group in groups.keys():
        groups[group] = Group.objects.get_or_create(name=group)[0]
        groups[group].save()

    permission_chief_administrator_list = (
        'Can add label', 'Can change label', 'Can delete label',
        'Can view label', 'Can add statistics plotter',
        'Can change statistics plotter', 'Can delete statistics plotter',
        'Can view statistics plotter', 'Can add statistics template',
        'Can change statistics template', 'Can delete statistics template',
        'Can view statistics template', 'Can add plotter',
        'Can change plotter', 'Can delete plotter', 'Can view plotter',
        'Can add template', 'Can change template', 'Can delete template',
        'Can view template', 'Can add user', 'Can change user',
        'Can delete user', 'Can view user',
    )
    permission_administrator_list = (
        'Can add plotter', 'Can change plotter', 'Can delete plotter',
        'Can view plotter', 'Can add template', 'Can change template',
        'Can delete template', 'Can view template', 'Can add user',
        'Can change user', 'Can delete user', 'Can view user',
        'Can add label', 'Can change label', 'Can delete label',
        'Can view label', 'Can view statistics plotter',
        'Can view statistics template', 'Can view cutting transaction',
    )

    permission_dealer_list = (
        'Can add user', 'Can change user', 'Can add plotter',
        'Can change plotter', 'Can view plotter', 'Can view user',
    )

    permission_user_list = (
        'Can view plotter', 'Can view statistics plotter',
    )

    permission_dealer = Permission.objects.filter(
        name__in=permission_dealer_list
    )
    permission_user = Permission.objects.filter(
        name__in=permission_user_list
    )
    permission_administrator = Permission.objects.filter(
        name__in=permission_administrator_list
    )
    permission_chief_administrator = Permission.objects.filter(
        name__in=permission_chief_administrator_list
    )
    groups[
        'Chief_Administrator'].permissions.add(*permission_chief_administrator)
    groups['Administrator'].permissions.add(*permission_administrator)
    groups['Dealer'].permissions.add(*permission_dealer)
    groups['User'].permissions.add(*permission_user)
    groups['Chief_Administrator'].save()
    groups['Administrator'].save()
    groups['User'].save()
    groups['Dealer'].save()


class Migration(migrations.Migration):

    dependencies = [("users", "0002_auto_20201015_1040")]

    operations = [migrations.RunPython(create_group)]

# Generated by Django 3.0.10 on 2020-11-23 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_techspec_group_and_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dealer',
            field=models.ForeignKey(help_text='Dealer who suplies user with stuff. Only for `User` role only.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attached_users', to=settings.AUTH_USER_MODEL, verbose_name='Dealer'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('Administrator', 'Administrator'), ('Dealer', 'Dealer'), ('Technical_Specialist', 'Technical_Specialist'), ('User', 'User')], help_text="User's role defines all allowed actions and permissions of the user in system.", max_length=30, null=True, verbose_name='User role'),
        ),
    ]
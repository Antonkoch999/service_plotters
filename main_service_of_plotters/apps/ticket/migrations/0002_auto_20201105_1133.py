# Generated by Django 3.0.10 on 2020-11-05 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='assignee',
            field=models.ForeignKey(blank=True, help_text='Technical Specialist who manage ticket', limit_choices_to={'role': 'Technical_Specialist'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Assignee'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='media_file',
            field=models.FileField(blank=True, null=True, upload_to='ticket_media/', verbose_name='Attached media file'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='reporter',
            field=models.ForeignKey(help_text='User who create ticket', limit_choices_to={'role': 'User'}, on_delete=django.db.models.deletion.CASCADE, related_name='created_tickets', to=settings.AUTH_USER_MODEL, verbose_name='Reporter'),
        ),
    ]

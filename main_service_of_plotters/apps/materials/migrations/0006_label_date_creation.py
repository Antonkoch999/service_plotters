# Generated by Django 3.0.10 on 2020-10-19 11:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_auto_20201019_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='date_creation',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data of creation label'),
        ),
    ]

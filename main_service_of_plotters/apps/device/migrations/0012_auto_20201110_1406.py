# Generated by Django 3.0.10 on 2020-11-10 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0011_plotter_device_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotter',
            name='device_id',
            field=models.CharField(max_length=15),
        ),
    ]

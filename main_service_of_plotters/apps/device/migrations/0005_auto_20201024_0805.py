# Generated by Django 3.0.10 on 2020-10-24 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0004_auto_20201022_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plotter',
            name='date_update',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]

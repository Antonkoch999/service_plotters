# Generated by Django 3.0.10 on 2020-10-24 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0004_auto_20201024_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuttingtransaction',
            name='date_update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='statisticsplotter',
            name='date_update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='statisticstemplate',
            name='date_update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]

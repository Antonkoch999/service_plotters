# Generated by Django 3.0.10 on 2020-11-05 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0030_auto_20201103_1407'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='label',
            name='size',
        ),
    ]

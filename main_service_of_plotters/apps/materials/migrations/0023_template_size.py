# Generated by Django 3.0.10 on 2020-11-03 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0022_auto_20201103_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='size',
            field=models.BooleanField(blank=True, choices=[(True, 'M'), (False, 'S')], null=True),
        ),
    ]

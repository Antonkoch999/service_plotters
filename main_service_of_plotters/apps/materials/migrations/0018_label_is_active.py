# Generated by Django 3.0.10 on 2020-10-27 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0017_auto_20201026_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.0.10 on 2020-10-22 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0007_label_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='date_update',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='template',
            name='date_update',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]

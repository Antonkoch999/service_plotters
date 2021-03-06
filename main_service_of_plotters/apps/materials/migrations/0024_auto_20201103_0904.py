# Generated by Django 3.0.10 on 2020-11-03 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0023_template_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='size',
            field=models.CharField(blank=True, choices=[('M', 'M'), ('S', 'S')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='template',
            name='size',
            field=models.CharField(blank=True, choices=[('M', 'M'), ('S', 'S')], max_length=1, null=True),
        ),
    ]

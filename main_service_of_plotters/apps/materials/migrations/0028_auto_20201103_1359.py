# Generated by Django 3.0.10 on 2020-11-03 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0027_auto_20201103_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='size',
            field=models.CharField(blank=True, choices=[('M', 'M'), ('S', 'S')], max_length=1, null=True, verbose_name='Size'),
        ),
    ]
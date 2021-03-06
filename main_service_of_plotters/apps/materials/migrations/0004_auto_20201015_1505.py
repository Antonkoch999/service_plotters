# Generated by Django 3.0.10 on 2020-10-15 15:05

from django.db import migrations, models
import main_service_of_plotters.apps.materials.validators


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0003_auto_20201015_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='barcode',
            field=models.CharField(blank=True, max_length=16, validators=[
                main_service_of_plotters.apps.materials.validators.validate_unique_code], verbose_name='Unique barcode'),
        ),
        migrations.AlterField(
            model_name='label',
            name='scratch_code',
            field=models.CharField(blank=True, max_length=16, validators=[
                main_service_of_plotters.apps.materials.validators.validate_unique_code], verbose_name='Unique scratch code'),
        ),
    ]

# Generated by Django 3.0.10 on 2020-10-15 13:32

from django.db import migrations, models
import django.db.models.deletion
import main_service_of_plotters.materials.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=60, verbose_name='category template')),
                ('date_creation', models.DateField(verbose_name='date of creation template')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='name of template')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scratch_code', models.CharField(blank=True, max_length=16, unique=True, validators=[main_service_of_plotters.materials.validators.validate_unique_code], verbose_name='Unique scratch code')),
                ('barcode', models.CharField(blank=True, max_length=16, unique=True, validators=[main_service_of_plotters.materials.validators.validate_unique_code], verbose_name='Unique barcode')),
                ('date_creation', models.DateField(verbose_name='Data of creation label')),
                ('date_life', models.DateField(verbose_name='Lifetime of label')),
                ('count', models.IntegerField()),
                ('lot', models.IntegerField()),
                ('size', models.CharField(blank=True, max_length=150, verbose_name='Size of label')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.Template', verbose_name='instance model template')),
            ],
            options={
                'unique_together': {('scratch_code', 'barcode')},
            },
        ),
    ]

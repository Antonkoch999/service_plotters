# Generated by Django 3.0.10 on 2020-10-15 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('device', '0001_initial'),
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticsPlotter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IP', models.CharField(max_length=150, verbose_name='IP address plotter')),
                ('last_request', models.DateField(verbose_name='last connection to server')),
                ('count_cut', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StatisticsTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('plotter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.Plotter', verbose_name='instance model plotter')),
                ('template_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.Template', verbose_name='instance model template')),
            ],
        ),
    ]

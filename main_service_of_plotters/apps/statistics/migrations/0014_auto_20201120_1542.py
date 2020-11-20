# Generated by Django 3.0.10 on 2020-11-20 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0013_auto_20201120_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statisticsplotter',
            name='count_cut',
            field=models.IntegerField(help_text='Count cut on plotter', verbose_name='Count cut'),
        ),
        migrations.AlterField(
            model_name='statisticstemplate',
            name='count',
            field=models.IntegerField(help_text='Count cut template on plotter', verbose_name='Count'),
        ),
    ]

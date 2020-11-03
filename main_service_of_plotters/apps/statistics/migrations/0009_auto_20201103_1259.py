# Generated by Django 3.0.10 on 2020-11-03 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0013_auto_20201103_1259'),
        ('statistics', '0008_auto_20201103_0829'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cuttingtransaction',
            options={'verbose_name': 'Cutting Transaction', 'verbose_name_plural': 'Cutting Transactions'},
        ),
        migrations.AlterModelOptions(
            name='statisticsplotter',
            options={'verbose_name': 'Plotter statistic', 'verbose_name_plural': 'Plotter statistics'},
        ),
        migrations.AlterModelOptions(
            name='statisticstemplate',
            options={'verbose_name': 'Template Statistic', 'verbose_name_plural': 'Template Statistics'},
        ),
        migrations.AlterField(
            model_name='cuttingtransaction',
            name='plotter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.Plotter', verbose_name='Plotter'),
        ),
        migrations.AlterField(
            model_name='statisticsplotter',
            name='count_cut',
            field=models.IntegerField(verbose_name='Count cut'),
        ),
        migrations.AlterField(
            model_name='statisticstemplate',
            name='count',
            field=models.IntegerField(verbose_name='Count'),
        ),
    ]

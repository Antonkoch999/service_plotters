# Generated by Django 3.0.10 on 2020-11-05 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20201105_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='popularproblem',
            name='name',
            field=models.CharField(help_text='Short name of porblem, will be displaied', max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='popularproblem',
            name='populated_text',
            field=models.TextField(blank=True, help_text='Text what will be populated in created ticket text', verbose_name='Populated Text'),
        ),
    ]

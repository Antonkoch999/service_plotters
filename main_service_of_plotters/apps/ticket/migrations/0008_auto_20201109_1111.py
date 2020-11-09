# Generated by Django 3.0.10 on 2020-11-09 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0007_auto_20201109_0916'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'permissions': [('can_report_problem', 'Can report a problem'), ('can_close_ticket', 'Can change ticket status to Close')], 'verbose_name': 'Ticket', 'verbose_name_plural': 'Tickets'},
        ),
        migrations.AlterField(
            model_name='popularproblem',
            name='name',
            field=models.CharField(help_text='Short name of problem, will be displayed', max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='answer_attached_file',
            field=models.FileField(blank=True, help_text='Media file attached by assigned technical specialist', null=True, upload_to='ticket_media/', verbose_name='Answer media file'),
        ),
    ]

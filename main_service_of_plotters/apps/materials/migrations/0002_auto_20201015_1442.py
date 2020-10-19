# Generated by Django 3.0.10 on 2020-10-15 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='label',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='label',
            constraint=models.UniqueConstraint(fields=('scratch_code', 'barcode'), name='scratch_code-barcode'),
        ),
    ]

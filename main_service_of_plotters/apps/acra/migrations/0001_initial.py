# Generated by Django 3.0.10 on 2020-11-24 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrashReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stack_trace', models.TextField(default='')),
                ('logcat', models.TextField(default='')),
                ('shared_preferences', models.TextField(default='')),
                ('environment', models.TextField(default='')),
                ('total_mem_size', models.BigIntegerField(default=0, verbose_name='Total Memory Size')),
                ('initial_configuration', models.TextField(default='')),
                ('display', models.TextField(default='')),
                ('available_mem_size', models.BigIntegerField(default=0, verbose_name='Available Memory Size')),
                ('phone_model', models.CharField(default='', max_length=50)),
                ('user_comment', models.TextField(default='')),
                ('crash_configuration', models.TextField(default='')),
                ('device_features', models.TextField(default='')),
                ('settings_system', models.TextField(default='', verbose_name='System Settings')),
                ('file_path', models.CharField(default='', max_length=100)),
                ('installation_id', models.CharField(default='', max_length=100)),
                ('user_crash_date', models.CharField(default='', max_length=50, verbose_name='Crash Date')),
                ('app_version_name', models.CharField(default='', max_length=50, verbose_name='Version Name')),
                ('user_app_start_date', models.CharField(default='', max_length=50, verbose_name='Application Start Date')),
                ('settings_global', models.TextField(default='', verbose_name='Global Settings')),
                ('build', models.TextField(default='')),
                ('settings_secure', models.TextField(default='', verbose_name='Secure Settings')),
                ('dumpsys_meminfo', models.TextField(default='')),
                ('user_email', models.CharField(default='', max_length=50)),
                ('report_id', models.CharField(default='', max_length=100)),
                ('product', models.CharField(default='', max_length=50)),
                ('package_name', models.CharField(default='', max_length=100, verbose_name='Package Name')),
                ('brand', models.CharField(default='', max_length=50)),
                ('android_version', models.CharField(default='', max_length=50)),
                ('app_version_code', models.CharField(default='', max_length=50, verbose_name='Version Code')),
                ('is_silent', models.CharField(default='', max_length=50)),
                ('custom_data', models.TextField(default='')),
                ('description', models.TextField(default='')),
                ('solved', models.CharField(choices=[('solved', 'Solved'), ('unsolved', 'Unsolved')], default='unsolved', max_length=10, verbose_name='Status')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

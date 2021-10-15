# Generated by Django 3.2.8 on 2021-10-15 13:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('link', models.URLField(blank=True, help_text='Link to your service / app (used to create link on status page)', null=True, verbose_name='Link')),
                ('interval', models.IntegerField(default=30, verbose_name='Interval (in seconds)')),
                ('timeout', models.IntegerField(default=30, verbose_name='Timeout (in seconds)')),
                ('pos', models.IntegerField(default=0, verbose_name='Positon on statuspage')),
                ('check_method', models.CharField(choices=[('HTTP', 'HTTP')], default='HTTP', max_length=10, verbose_name='Check service method')),
                ('url', models.URLField(blank=True, help_text='Url to checking your service', null=True, verbose_name='Url')),
                ('status', models.BooleanField(default=False, verbose_name='Service Status')),
                ('next_check', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_check_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
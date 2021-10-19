# Generated by Django 3.2.8 on 2021-10-19 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_service_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceCheck',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('latency', models.IntegerField(default=0)),
                ('online', models.BooleanField(default=False)),
                ('datetime', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicechecks', related_query_name='servicecheck', to='app.service')),
            ],
        ),
    ]

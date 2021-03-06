# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-15 14:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0003_auto_20160414_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledRepark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('picked_up_at', models.DateTimeField(blank=True, null=True)),
                ('enroute_at', models.DateTimeField(blank=True, null=True)),
                ('dropped_off_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('in_progress', models.BooleanField(default=False)),
                ('is_completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('scheduled_start_date', models.DateField()),
                ('scheduled_end_date', models.DateField()),
                ('time_limit', models.IntegerField()),
                ('parking_exp_time', models.DateTimeField()),
                ('dropoff_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_scheduledrepark_dropoff_loc_related', to='locations.Location', verbose_name='dropoff location')),
                ('pickup_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_scheduledrepark_pickup_loc_related', to='locations.Location', verbose_name='pickup location')),
                ('reparked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_scheduledrepark_valet_related', to=settings.AUTH_USER_MODEL, verbose_name='valet')),
                ('requested_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_scheduledrepark_customer_related', to=settings.AUTH_USER_MODEL, verbose_name='customer')),
                ('valet_start_pos', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_scheduledrepark_related', to='locations.Location')),
            ],
            options={
                'db_table': 'scheduled_reparks',
            },
        ),
    ]

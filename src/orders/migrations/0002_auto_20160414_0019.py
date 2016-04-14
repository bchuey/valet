# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-14 00:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dropoff',
            name='valet_starting_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_dropoff_starting_loc', to='locations.Location', verbose_name='starting location'),
        ),
        migrations.AlterField(
            model_name='repark',
            name='valet_starting_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_repark_starting_loc', to='locations.Location', verbose_name='starting location'),
        ),
    ]
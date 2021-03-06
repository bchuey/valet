# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-17 14:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterectionLatLng',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.CharField(blank=True, max_length=255, null=True, verbose_name='latitude')),
                ('lng', models.CharField(blank=True, max_length=255, null=True, verbose_name='longitude')),
            ],
            options={
                'db_table': 'intersections',
            },
        ),
        migrations.CreateModel(
            name='ParkingSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=1)),
                ('time_limit', models.IntegerField()),
            ],
            options={
                'db_table': 'parking_sections',
            },
        ),
        migrations.AddField(
            model_name='interectionlatlng',
            name='parking_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='latlngs', to='locations.ParkingSection'),
        ),
    ]

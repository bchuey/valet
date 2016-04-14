# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-13 20:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_is_valet'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriversLicense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legal_first_name', models.CharField(max_length=60)),
                ('legal_last_name', models.CharField(max_length=60)),
                ('date_of_birth', models.DateField()),
                ('license_id_number', models.CharField(max_length=60)),
                ('registered_city', models.CharField(max_length=100)),
                ('registered_state', models.CharField(max_length=25)),
                ('owned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'driver_licenses',
            },
        ),
        migrations.CreateModel(
            name='InsurancePolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=30)),
                ('policy_number', models.CharField(max_length=50)),
                ('agent_first_name', models.CharField(max_length=25)),
                ('agent_last_name', models.CharField(max_length=25)),
                ('agent_phone_number', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'insurance_policies',
            },
        ),
        migrations.CreateModel(
            name='RegisteredVehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=60)),
                ('model', models.CharField(max_length=60)),
                ('color', models.CharField(max_length=60)),
                ('year', models.CharField(blank=True, max_length=4, null=True)),
                ('license_plate_number', models.CharField(max_length=10)),
                ('updated_registration_tags', models.BooleanField(default=True)),
                ('owned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'registered_vehicles',
            },
        ),
        migrations.AddField(
            model_name='insurancepolicy',
            name='insured_vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.RegisteredVehicle'),
        ),
        migrations.AddField(
            model_name='insurancepolicy',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

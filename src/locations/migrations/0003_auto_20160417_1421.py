# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-17 14:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20160417_1420'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='InterectionLatLng',
            new_name='IntersectionLatLng',
        ),
    ]

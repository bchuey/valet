# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-30 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20160427_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic_medium',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pic_small',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
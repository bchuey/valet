# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-18 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_auto_20160418_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingsection',
            name='label',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('BB', 'BB'), ('C', 'C'), ('CC', 'CC'), ('D', 'D'), ('DD', 'DD'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), ('I', 'I'), ('J', 'J'), ('K', 'K'), ('L', 'L'), ('M', 'M'), ('N', 'N'), ('O', 'O'), ('P', 'P'), ('Q', 'Q'), ('R', 'R'), ('S', 'S'), ('T', 'T'), ('U', 'U'), ('V', 'V'), ('W', 'W'), ('X', 'X'), ('Y', 'Y'), ('Z', 'Z')], max_length=2),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-22 02:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20170922_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 22, 3, 50, 45, 853593)),
        ),
    ]
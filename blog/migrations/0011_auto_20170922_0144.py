# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-22 00:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20170907_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 22, 1, 44, 25, 442079)),
        ),
    ]

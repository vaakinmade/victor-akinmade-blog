# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-30 13:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20170930_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 9, 30, 14, 19, 43, 342136)),
        ),
    ]
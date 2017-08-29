# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-17 21:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20170802_0336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='read_minutes',
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.CharField(default='', max_length=225),
        ),
        migrations.AlterField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
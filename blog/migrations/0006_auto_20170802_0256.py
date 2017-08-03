# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 01:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.crypto


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_lookup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='lookup',
            field=models.SlugField(default=django.utils.crypto.get_random_string, unique=True),
        ),
    ]
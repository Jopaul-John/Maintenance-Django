# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-22 03:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_devicehistory_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicehistory',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-22 03:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicehistory',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 22, 3, 31, 30, 905042, tzinfo=utc)),
        ),
    ]

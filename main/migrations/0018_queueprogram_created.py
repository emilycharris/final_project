# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 04:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20160725_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='queueprogram',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 7, 26, 4, 2, 15, 520944, tzinfo=utc)),
            preserve_default=False,
        ),
    ]

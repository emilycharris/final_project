# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 22:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20160725_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='queueprogram',
            name='program',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Program'),
        ),
    ]

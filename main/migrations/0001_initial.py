# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 13:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child', to='main.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('guidebox_id', models.IntegerField()),
                ('runtime', models.IntegerField()),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='program_thumbnails')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='program_banners')),
                ('overview', models.TextField()),
                ('review', models.TextField()),
                ('positive_message', models.TextField()),
                ('positive_role_model', models.TextField()),
                ('violence', models.TextField()),
                ('sex', models.TextField()),
                ('language', models.TextField()),
                ('consumerism', models.TextField()),
                ('substance', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QueueProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('program', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Program')),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Queue')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(max_length=10)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('detail', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='program',
            name='rating',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Rating'),
        ),
        migrations.AddField(
            model_name='profile',
            name='rating_limit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Rating'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

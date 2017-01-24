# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 13:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ups', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='date_added',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='project_desc',
            new_name='desc',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='project_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='server_addr',
            new_name='addr',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='date_added',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='server_desc',
            new_name='desc',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='server_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='server_wdir',
            new_name='wdir',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-10-17 19:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooggerapp', '0003_auto_20171017_2250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfollow',
            old_name='site',
            new_name='adress',
        ),
        migrations.RenameField(
            model_name='userfollow',
            old_name='web_site',
            new_name='choices',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-02-03 06:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0009_filebean_user_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filebean',
            name='user_post',
        ),
        migrations.DeleteModel(
            name='FileBean',
        ),
    ]

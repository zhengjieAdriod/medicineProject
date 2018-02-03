# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-02-03 06:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0008_filebean'),
    ]

    operations = [
        migrations.AddField(
            model_name='filebean',
            name='user_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medicine.User'),
        ),
    ]

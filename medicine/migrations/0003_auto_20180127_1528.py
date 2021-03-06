# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-27 07:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0002_auto_20180125_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='subjects_for_followers', to='medicine.User'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='initiator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subjects_for_initiator', to='medicine.User'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-02-03 07:56
from __future__ import unicode_literals

from django.db import migrations, models
import medicine.models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0011_filebean'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='content',
            field=models.FileField(blank=True, upload_to=medicine.models.user_directory_path),
        ),
    ]

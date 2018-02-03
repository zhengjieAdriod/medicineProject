# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-02-03 06:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import medicine.models


class Migration(migrations.Migration):

    dependencies = [
        ('medicine', '0010_auto_20180203_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileBean',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('des', models.TextField(blank=True, default='文件描述')),
                ('post_time', models.DateTimeField(auto_now_add=True)),
                ('path', models.FileField(blank=True, upload_to=medicine.models.user_directory_path)),
                ('user_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medicine.User')),
            ],
            options={
                'ordering': ['-post_time'],
            },
        ),
    ]
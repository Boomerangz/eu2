# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 22:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='url',
            field=models.URLField(default='http://google.com'),
            preserve_default=False,
        ),
    ]

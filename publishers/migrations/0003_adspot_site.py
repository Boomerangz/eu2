# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 20:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publishers', '0002_site_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='adspot',
            name='site',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='publishers.Site'),
        ),
    ]

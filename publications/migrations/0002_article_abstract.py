# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-16 08:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='abstract',
            field=models.TextField(blank=True, help_text='Enter Abstract here', max_length=256),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 10:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lexicon', '0133_auto_20161219_1040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lexeme',
            old_name='source_form',
            new_name='romanised',
        ),
    ]

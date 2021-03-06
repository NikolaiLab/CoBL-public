# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-16 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lexicon', '0154_language_fragmentary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cognateclass',
            name='name',
        ),
        migrations.AddField(
            model_name='cognateclass',
            name='alsoUsedInOtherMeanings',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='cognateclass',
            name='justificationDiscussion',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='cognateclasscitation',
            name='rfcWeblink',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='meaning',
            name='concepticon_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='nexusexport',
            name='_exportMatrix',
            field=models.BinaryField(null=True),
        ),
        migrations.AddField(
            model_name='nexusexport',
            name='calculateMatrix',
            field=models.BooleanField(default=False),
        ),
    ]

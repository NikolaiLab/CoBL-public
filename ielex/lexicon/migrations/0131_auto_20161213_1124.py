# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-13 11:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lexicon', '0130_copy_hindi_transliteration_to_urdu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='lastEditedBy',
            field=models.CharField(default='unknown', max_length=32),
        ),
        migrations.AlterField(
            model_name='clade',
            name='distribution',
            field=models.CharField(choices=[
                ('U', 'Uniform'),
                ('N', 'Normal'),
                ('L', 'Log normal'),
                ('O', 'Offset log normal'),
                ('_', 'None')], default='_', max_length=1),
        ),
        migrations.AlterField(
            model_name='clade',
            name='lastEditedBy',
            field=models.CharField(default='unknown', max_length=32),
        ),
        migrations.AlterField(
            model_name='cognateclass',
            name='lastEditedBy',
            field=models.CharField(default='unknown', max_length=32),
        ),
        migrations.AlterField(
            model_name='cognateclass',
            name='proposedAsCognateToScale',
            field=models.IntegerField(choices=[
                (0, '1/6=small minority view'),
                (1, '2/6=sig. minority view'),
                (2, '3/6=50/50 balance'),
                (3, '4/6=small majority view'),
                (4, '5/6=large majority view')], default=0),
        ),
        migrations.AlterField(
            model_name='cognateclass',
            name='revisedBy',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='cognateclasscitation',
            name='reliability',
            field=models.CharField(choices=[
                ('A', 'High'),
                ('B', 'Good (e.g. should be double checked)'),
                ('C', 'Doubtful'),
                ('L', 'Loanword'),
                ('X', 'Exclude (e.g. not the Swadesh term)')], max_length=1),
        ),
        migrations.AlterField(
            model_name='cognatejudgement',
            name='lastEditedBy',
            field=models.CharField(default='unknown', max_length=32),
        ),
        migrations.AlterField(
            model_name='cognatejudgementcitation',
            name='reliability',
            field=models.CharField(choices=[
                ('A', 'High'),
                ('B', 'Good (e.g. should be double checked)'),
                ('C', 'Doubtful'),
                ('L', 'Loanword'),
                ('X', 'Exclude (e.g. not the Swadesh term)')], max_length=1),
        ),
        migrations.AlterField(
            model_name='language',
            name='distribution',
            field=models.CharField(choices=[
                ('U', 'Uniform'),
                ('N', 'Normal'),
                ('L', 'Log normal'),
                ('O', 'Offset log normal'),
                ('_', 'None')], default='_', max_length=1),
        ),
        migrations.AlterField(
            model_name='language',
            name='lastEditedBy',
            field=models.CharField(default='unknown', max_length=32),
        ),
        migrations.AlterField(
            model_name='language',
            name='progress',
            field=models.IntegerField(choices=[
                (0, 'No data'),
                (1, 'Highly problematic'),
                (2, 'Limited revision, still unreliable'),
                (3, 'Revision underway'),
                (4, 'Revision complete'),
                (5, 'Second review complete')], default=0),
        ),
        migrations.AlterField(
            model_name='lexeme',
            name='lastEditedBy',
            field=models.CharField(default='unknown', max_length=32),
        ),
        migrations.AlterField(
            model_name='lexemecitation',
            name='reliability',
            field=models.CharField(choices=[
                ('A', 'High'),
                ('B', 'Good (e.g. should be double checked)'),
                ('C', 'Doubtful'),
                ('L', 'Loanword'),
                ('X', 'Exclude (e.g. not the Swadesh term)')], max_length=1),
        ),
        migrations.AlterField(
            model_name='meaning',
            name='lastEditedBy',
            field=models.CharField(default='unknown', max_length=32),
        ),
        migrations.AlterField(
            model_name='nexusexport',
            name='lastEditedBy',
            field=models.CharField(default='unknown', max_length=32),
        ),
        migrations.AlterField(
            model_name='sndcomp',
            name='lastEditedBy',
            field=models.CharField(default='unknown', max_length=32),
        ),
        migrations.AlterField(
            model_name='source',
            name='TRS',
            field=models.BooleanField(
                default=False,
                help_text='Traditional reference source (dated).'),
        ),
        migrations.AlterField(
            model_name='source',
            name='respect',
            field=models.TextField(
                blank=True,
                help_text='A brief summary of the nature '
                          'of the source its utility.'),
        ),
    ]
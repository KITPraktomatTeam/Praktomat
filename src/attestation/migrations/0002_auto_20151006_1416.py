# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
        ('accounts', '0001_initial'),
        ('solutions', '0001_initial'),
        ('attestation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='attestation',
            name='author',
            field=models.ForeignKey(verbose_name=b'attestation author', to='accounts.User'),
        ),
        migrations.AddField(
            model_name='attestation',
            name='final_grade',
            field=models.ForeignKey(to='attestation.RatingScaleItem', help_text='The mark for the whole solution.', null=True),
        ),
        migrations.AddField(
            model_name='attestation',
            name='solution',
            field=models.ForeignKey(to='solutions.Solution'),
        ),
        migrations.AddField(
            model_name='annotatedsolutionfile',
            name='attestation',
            field=models.ForeignKey(to='attestation.Attestation'),
        ),
        migrations.AddField(
            model_name='annotatedsolutionfile',
            name='solution_file',
            field=models.ForeignKey(to='solutions.SolutionFile'),
        ),
    ]

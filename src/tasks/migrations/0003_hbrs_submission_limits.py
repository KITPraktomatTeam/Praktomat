# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_merge-hbrs'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='submission_free_uploads',
            field=models.IntegerField(default=1, help_text='Number of submissions a user can make before waitdelta got active'),
        ),
        migrations.AddField(
            model_name='task',
            name='submission_maxpossible',
            field=models.IntegerField(default=-1, help_text='Number of uploads a user can submit for the same task. Value -1 means unlimited'),
        ),
        migrations.AddField(
            model_name='task',
            name='submission_waitdelta',
            field=models.IntegerField(default=0, help_text='Timedelta in minutes. The user must wait before submitting the next solution of same task: Timedelta multiplied with number of current uploads'),
        ),
    ]

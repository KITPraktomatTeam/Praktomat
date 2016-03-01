# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='jplag_up_to_date',
            field=models.BooleanField(default=False, help_text='No new solution uploads since the last jPlag run'),
        ),
    ]

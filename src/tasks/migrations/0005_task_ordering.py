# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_task_warning_threshold'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['submission_date', 'title']},
        ),
    ]

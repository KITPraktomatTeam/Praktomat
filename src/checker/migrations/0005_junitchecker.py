# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_jplag_up_to_date'),
        ('checker', '0004_textchecker_and_scalabuilder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='junitchecker',
            name='ignore',
            field=models.CharField(blank=True, default='', help_text='space-separated list of files to be ignored during compilation, i.e.: these files will not be compiled.', max_length=4096),
        ),
    ]

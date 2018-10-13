# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import os.path


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0005_auto_20170404_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='scriptchecker',
            name='filename',
            field=models.CharField(help_text='What the file will be named in the sandbox. If empty, we try to guess the right filename!', max_length=500, blank=True, default=""),
        ),
    ]



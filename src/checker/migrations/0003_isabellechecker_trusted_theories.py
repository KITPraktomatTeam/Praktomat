# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0002_auto_20151006_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='isabellechecker',
            name='trusted_theories',
            field=models.CharField(help_text='Isabelle theories to be run in trusted mode (Library theories or theories uploaded using the Create File Checker). Do not include the file extensions. Separate multiple theories by space', max_length=200, blank=True),
        ),
    ]

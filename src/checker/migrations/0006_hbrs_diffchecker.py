# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import checker.basemodels


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0005_merge_hbrs_jplag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diffchecker',
            name='shell_script',
            field=checker.basemodels.CheckerFileField(help_text='The shell script whose output for the given input file is compared to the given output file: The substrings JAVA and PROGRAM got replaced by Praktomat determined values.', max_length=500, upload_to=checker.basemodels.get_checkerfile_storage_path),
        ),
    ]

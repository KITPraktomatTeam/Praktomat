# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0006_auto_20170405_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='createfilechecker',
            name='include_in_solution_download',
            field=models.BooleanField(default=True, help_text='The file is (or, if it is a zipfile to be unpacked: its content) is included in "full" solution download .zip files'),
        ),
        migrations.AddField(
            model_name='haskelltestframeworkchecker',
            name='include_in_solution_download',
            field=models.BooleanField(default=True, help_text='The file is (or, if it is a zipfile to be unpacked: its content) is included in "full" solution download .zip files'),
        ),
    ]

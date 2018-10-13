# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0004_textchecker_and_scalabuilder'),
    ]

    operations = [
        migrations.AddField(
            model_name='createfilechecker',
            name='is_sourcecode',
            field=models.BooleanField(default=False, help_text='The file is (or, if it is a zipfile to be unpacked: contains) source code'),
        ),
        migrations.AddField(
            model_name='haskelltestframeworkchecker',
            name='is_sourcecode',
            field=models.BooleanField(default=False, help_text='The file is (or, if it is a zipfile to be unpacked: contains) source code'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0006_settings_warning_message_chunk'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='final_grades_arithmetic_option',
            field=models.CharField(default=b'SUM', max_length=3, choices=[(b'SUM', b'Sum'), (b'AVG', b'Average')]),
        ),
        migrations.AddField(
            model_name='settings',
            name='final_grades_plagiarism_option',
            field=models.CharField(default=b'NP', max_length=2, choices=[(b'NP', b'Without'), (b'WP', b'Including')]),
        ),
    ]

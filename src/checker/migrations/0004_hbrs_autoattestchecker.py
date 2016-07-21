# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0003_merge-hbrs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoattestchecker',
            name='final',
            field=models.BooleanField(default=True, help_text='Indicates whether the attestation is ready to be published'),
        ),
        migrations.AlterField(
            model_name='autoattestchecker',
            name='published',
            field=models.BooleanField(default=True, help_text='Indicates whether the user can see the attestation.'),
        ),
    ]

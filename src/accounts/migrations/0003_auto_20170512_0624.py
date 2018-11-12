# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_add_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mat_number',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[accounts.models.validate_mat_number]),
        ),
    ]

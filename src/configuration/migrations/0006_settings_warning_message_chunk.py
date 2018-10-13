# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def settings_warning_message_chunk(apps, schema_editor):
    Chunk = apps.get_model("configuration", "Chunk")
    Chunk.objects.get_or_create(key="warning message")[0].save()



class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0005_settings_inactive_chunk'),
    ]

    operations = [
        migrations.RunPython(settings_warning_message_chunk),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def initial_configuration(apps, schema_editor):
    Settings = apps.get_model("configuration", "Settings")
    conf = Settings.objects.get_or_create()[0]
    conf.save()

    Chunk = apps.get_model("configuration", "Chunk")
    Chunk.objects.get_or_create(key="Welcome Message")[0].save()
    Chunk.objects.get_or_create(key="Login Message")[0].save()



class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_configuration),
    ]

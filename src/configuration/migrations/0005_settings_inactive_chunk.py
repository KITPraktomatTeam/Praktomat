# -*- coding: utf-8 -*-


from django.db import migrations, models

def settings_inactive_chunk(apps, schema_editor):
    Chunk = apps.get_model("configuration", "Chunk")
    Chunk.objects.get_or_create(key="inactive user")[0].save()



class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0004_settings_jplag_setting'),
    ]

    operations = [
        migrations.RunPython(settings_inactive_chunk),
    ]

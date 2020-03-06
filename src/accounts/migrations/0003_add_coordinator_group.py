# -*- coding: utf-8 -*-


from django.db import migrations, models

def add_coordinator_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    coordinator = Group.objects.get_or_create(name="Coordinator")[0]
    coordinator.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_add_groups'),
    ]

    operations = [
        migrations.RunPython(add_coordinator_group)
    ]

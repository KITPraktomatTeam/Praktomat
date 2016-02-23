# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    trainer = Group.objects.get_or_create(name="Trainer")[0]
    Permissions = apps.get_model("auth", "Permission")
    permissions = Permissions.objects.filter(codename__in=[
        u'add_tutorial', u'change_tutorial', u'delete_tutorial',
        u'add_userprofile', u'change_userprofile', u'delete_userprofile',
        u'add_rating', u'change_rating', u'delete_rating',
        u'add_ratingaspect',  u'change_ratingaspect', u'delete_ratingaspect',
        u'add_ratingscale', u'change_ratingscale', u'delete_ratingscale',
        u'add_ratingscaleitem', u'change_ratingscaleitem', u'delete_ratingscaleitem',
        u'add_user', u'change_user', u'delete_user',
        u'add_mediafile', u'change_mediafile', u'delete_mediafile',
        u'add_task', u'change_task', u'delete_task',
        u'change_solution',
        u'change_chunk','change_settings',
        ])

    trainer.permissions.add(*permissions)
    trainer.save()

    tutor = Group.objects.get_or_create(name="Tutor")[0]
    tutor.save()
    user = Group.objects.get_or_create(name="User")[0]
    user.save()



class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_groups)
    ]

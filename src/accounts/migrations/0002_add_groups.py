# -*- coding: utf-8 -*-


from django.db import migrations, models

def add_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    trainer = Group.objects.get_or_create(name="Trainer")[0]
    Permissions = apps.get_model("auth", "Permission")
    permissions = Permissions.objects.filter(codename__in=[
        'add_tutorial', 'change_tutorial', 'delete_tutorial',
        'add_userprofile', 'change_userprofile', 'delete_userprofile',
        'add_rating', 'change_rating', 'delete_rating',
        'add_ratingaspect',  'change_ratingaspect', 'delete_ratingaspect',
        'add_ratingscale', 'change_ratingscale', 'delete_ratingscale',
        'add_ratingscaleitem', 'change_ratingscaleitem', 'delete_ratingscaleitem',
        'add_user', 'change_user', 'delete_user',
        'add_mediafile', 'change_mediafile', 'delete_mediafile',
        'add_task', 'change_task', 'delete_task',
        'change_solution',
        'change_chunk', 'change_settings',
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

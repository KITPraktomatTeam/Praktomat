# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
        ('solutions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='task',
            field=models.ForeignKey(to='tasks.Task', on_delete=models.CASCADE),
        ),
    ]

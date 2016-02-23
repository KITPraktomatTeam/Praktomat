# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0001_initial'),
        ('tasks', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('solutions', '0002_solution_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='textchecker',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='scriptchecker',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='rchecker',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='linewidthchecker',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='linecounter',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='keepfilechecker',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='junitchecker',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='javagccbuilder',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='javabuilder',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='isabellechecker',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='interfacechecker',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='haskelltestframeworkchecker',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='haskellbuilder',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='fortranbuilder',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='dejagnutester',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='dejagnusetup',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='cxxbuilder',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='createfilechecker',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='checkstylechecker',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='checkerresultartefact',
            name='result',
            field=models.ForeignKey(related_name='artefacts', to='checker.CheckerResult'),
        ),
        migrations.AddField(
            model_name='checkerresult',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='checkerresult',
            name='solution',
            field=models.ForeignKey(to='solutions.Solution'),
        ),
        migrations.AddField(
            model_name='cbuilder',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
        migrations.AddField(
            model_name='anonymitychecker',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
    ]

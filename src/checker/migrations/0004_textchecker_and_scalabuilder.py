# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_jplag_up_to_date'),
        ('checker', '0003_isabellechecker_trusted_theories'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScalaBuilder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('_flags', models.CharField(default=b'-Wall', help_text='Compiler flags', max_length=1000, blank=True)),
                ('_output_flags', models.CharField(default=b'-o %s', help_text="Output flags. '%s' will be replaced by the program name.", max_length=1000, blank=True)),
                ('_libs', models.CharField(default=b'', help_text='Compiler libraries', max_length=1000, blank=True)),
                ('_file_pattern', models.CharField(default=b'^[a-zA-Z0-9_]*$', help_text='Regular expression describing all source files to be passed to the compiler.', max_length=1000)),
                ('_main_required', models.BooleanField(default=True, help_text='Is a submission required to provide a main method?')),
                ('task', models.ForeignKey(to='tasks.Task')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='textchecker',
            name='choices',
            field=models.IntegerField(default=1, verbose_name=b'Select:', choices=[(0, b'The text must not be in the solution'), (1, b'The text has to be in the solution')]),
        ),
        migrations.AlterField(
            model_name='textchecker',
            name='text',
            field=models.TextField(),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import checker.basemodels


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_jplag_up_to_date'),
        ('checker', '0004_textchecker_and_scalabuilder'),
    ]

    operations = [
        migrations.CreateModel(
            name='JavaChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('class_name', models.CharField(help_text='The fully qualified name of the test case class (without .class)', max_length=100)),
                ('test_description', models.TextField(help_text='Description of the Testcase. To be displayed on Checker Results page when checker is unfolded.')),
                ('name', models.CharField(help_text='Name of the Testcase. To be displayed as title on Checker Results page', max_length=100)),
                ('task', models.ForeignKey(to='tasks.Task')),
            ],
            options={
                'abstract': False,
            },
        )
    ]

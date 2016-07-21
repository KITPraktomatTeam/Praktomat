# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import checker.basemodels


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_merge-hbrs'),
        ('accounts', '0002_add_groups'),
        ('checker', '0002_auto_20151006_1416'),
        ('checker', '0003_isabellechecker_trusted_theories'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoAttestChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('public_comment', models.TextField(help_text='Comment which is shown to the user.', blank=True)),
                ('private_comment', models.TextField(help_text='Comment which is only visible to tutors', blank=True)),
                ('final', models.BooleanField(default=False, help_text='Indicates whether the attestation is ready to be published')),
                ('published', models.BooleanField(default=False, help_text='Indicates whether the user can see the attestation.')),
                ('author', models.ForeignKey(verbose_name=b'attestation author', to='accounts.User')),
                ('task', models.ForeignKey(to='tasks.Task')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DiffChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('shell_script', checker.basemodels.CheckerFileField(help_text='The shell script whose output for the given input file is compared to the given output file.', max_length=500, upload_to=checker.basemodels.get_checkerfile_storage_path)),
                ('input_file', checker.basemodels.CheckerFileField(help_text='The file containing the input for the program.', max_length=500, upload_to=checker.basemodels.get_checkerfile_storage_path, blank=True)),
                ('output_file', checker.basemodels.CheckerFileField(help_text='The file containing the output for the program.', max_length=500, upload_to=checker.basemodels.get_checkerfile_storage_path, blank=True)),
                ('task', models.ForeignKey(to='tasks.Task')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='cbuilder',
            name='task',
        ),
        migrations.RemoveField(
            model_name='cxxbuilder',
            name='task',
        ),
        migrations.RemoveField(
            model_name='fortranbuilder',
            name='task',
        ),
        migrations.RemoveField(
            model_name='haskellbuilder',
            name='task',
        ),
        migrations.RemoveField(
            model_name='haskelltestframeworkchecker',
            name='task',
        ),
        migrations.RemoveField(
            model_name='ignoringhaskellbuilder',
            name='haskellbuilder_ptr',
        ),
        migrations.RemoveField(
            model_name='isabellechecker',
            name='task',
        ),
        migrations.RemoveField(
            model_name='rchecker',
            name='task',
        ),
        migrations.RemoveField(
            model_name='testonlybuildingbuilder',
            name='haskellbuilder_ptr',
        ),
        migrations.DeleteModel(
            name='CBuilder',
        ),
        migrations.DeleteModel(
            name='CXXBuilder',
        ),
        migrations.DeleteModel(
            name='FortranBuilder',
        ),
        migrations.DeleteModel(
            name='HaskellBuilder',
        ),
        migrations.DeleteModel(
            name='HaskellTestFrameWorkChecker',
        ),
        migrations.DeleteModel(
            name='IgnoringHaskellBuilder',
        ),
        migrations.DeleteModel(
            name='IsabelleChecker',
        ),
        migrations.DeleteModel(
            name='RChecker',
        ),
        migrations.DeleteModel(
            name='TestOnlyBuildingBuilder',
        ),
    ]

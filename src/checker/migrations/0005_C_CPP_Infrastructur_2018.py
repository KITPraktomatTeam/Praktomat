# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_jplag_up_to_date'),
        ('checker', '0004_textchecker_and_scalabuilder'),
    ]

    operations = [
        migrations.CreateModel(
            name='CLinker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('_main_required', models.BooleanField(default=True, help_text='Is a submission required to provide a main method or function?')),
                ('_libs', models.CharField(default=b'', help_text='Compiler libraries', max_length=1000, blank=True)),
                ('_search_path', models.CharField(default=b'', help_text='flags for additional search path for compiler or linker ', max_length=1000, blank=True)),
                ('_flags', models.CharField(default=b'-Wall -Wextra', help_text='Compiler or Linker flags', max_length=1000, blank=True)),
                ('_file_pattern', models.CharField(default=b'^[a-zA-Z0-9_]*$', help_text='Regular expression describing all source files to be passed to the compiler or linker. (Play with  RegEx at <a href="http://pythex.org/" target="_blank">http://pythex.org/ </a>', max_length=1000)),
                ('_output_flags', models.CharField(default=b'-o %s', help_text="choose link output type. '%s' will replaced by output_name. ", max_length=16, choices=[('out', '-o %s (Link to executable program)'), ('so', '-shared -fPIC -o %s (Link to shared object)')])),
                ('_output_name', models.CharField(default=b'%s', help_text="choose a outputname. '%s' will be replaced by an internal default name.", max_length=16)),
                ('task', models.ForeignKey(to='tasks.Task')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CUnitChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('class_name', models.CharField(help_text='The fully qualified name of the test case executable (with fileending like .exe or .out)', max_length=100)),
                ('test_description', models.TextField(help_text='Description of the Testcase. To be displayed on Checker Results page when checker is  unfolded.')),
                ('name', models.CharField(help_text='Name of the Testcase. To be displayed as title on Checker Results page', max_length=100)),
                ('ignore', models.CharField(default=b'', help_text='space-seperated list of files to be ignored during compilation, i.e.: these files will not be compiled.', max_length=4096, blank=True)),
                ('_flags', models.CharField(default=b'-Wall -Wextra', help_text='Compiler flags', max_length=1000, blank=True)),
                ('_libs', models.CharField(default=b'', help_text='Compiler libraries except cunit, cppunit', max_length=1000, blank=True)),
                ('cunit_version', models.CharField(default=b'cunit', max_length=16, choices=[(b'cunit', 'CUnit 2.1-3'), (b'cppunit', 'CppUnit 1.12.1')])),
                ('task', models.ForeignKey(to='tasks.Task')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CUnitChecker2',
            fields=[
                ('createfilechecker_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='checker.CreateFileChecker')),
                ('class_name', models.CharField(help_text='The fully qualified name of the test case executable (with fileending like .exe or .out)', max_length=100, verbose_name='TestApp Filename')),
                ('test_description', models.TextField(help_text='Description of the Testcase. To be displayed on Checker Results page when checker is  unfolded.')),
                ('name', models.CharField(help_text='Name of the Testcase. To be displayed as title on Checker Results page', max_length=100)),
                ('_ignore', models.CharField(default=b'', help_text='Regular Expression for ignoring files while compile and link test-code. Play with  RegEx at <a href="http://pythex.org/" target="_blank">http://pythex.org/ </a>', max_length=4096, blank=True)),
                ('_ignore_sol', models.CharField(default=b'', help_text='Regular Expression for ignoring files while compile and link solution-code.', max_length=4096, blank=True)),
                ('_flags', models.CharField(default=b'-Wall -Wextra', help_text='Compiler flags', max_length=1000, blank=True)),
                ('_libs', models.CharField(default=b'', help_text='Compiler libraries except cunit, cppunit', max_length=1000, blank=True)),
                ('link_type', models.CharField(default=b'o', help_text='How to use solution submission in test-code?', max_length=16, choices=[(b'o', 'Link Trainers Test-Code with solution objects (*.o)'), (b'so', 'Link solution objects as shared object (*.so, *.dll)'), (b'out', 'Link solution objects as seperate executable program (*.out, *.exe)')])),
                ('cunit_version', models.CharField(default=b'cunit', max_length=16, choices=[(b'cunit', 'CUnit 2.1-3'), (b'cppunit', 'CppUnit 1.12.1'), (b'c', 'C tests'), (b'cpp', 'CPP tests')])),
            ],
            options={
                'abstract': False,
            },
            bases=('checker.createfilechecker',),
        ),
        migrations.CreateModel(
            name='CUnitChecker3',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('name', models.CharField(help_text='Name of the Testcase. To be displayed as title on Checker Results page', max_length=100)),
                ('test_description', models.TextField(help_text='Description of the Testcase. To be displayed on Checker Results page when checker is  unfolded.')),
                ('class_name', models.CharField(help_text='The fully qualified name of the test case executable (with fileending like .exe or .out)', max_length=100, verbose_name='TestApp Filename')),
                ('_ignore', models.CharField(default=b'', help_text='Regular Expression for ignoring files while compile and link test-code.', max_length=4096, blank=True)),
                ('_ignore_sol', models.CharField(default=b'', help_text='Regular Expression for ignoring files while compile and link solution-code.', max_length=4096, blank=True)),
                ('_flags', models.CharField(default=b'-Wall -Wextra', help_text='Compiler flags', max_length=1000, blank=True)),
                ('_libs', models.CharField(default=b'', help_text='Compiler libraries except cunit, cppunit', max_length=1000, blank=True)),
                ('link_type', models.CharField(default=b'o', help_text='How to use solution submission in test-code?', max_length=16, choices=[(b'o', 'Link Trainers Test-Code with solution objects (*.o)'), (b'so', 'Link solution objects as shared object (*.so, *.dll)'), (b'out', 'Link solution objects as seperate executable program (*.out, *.exe)')])),
                ('cunit_version', models.CharField(default=b'cunit', max_length=16, choices=[(b'cunit', 'CUnit 2.1-3'), (b'cppunit', 'CppUnit 1.12.1'), (b'c', 'C tests'), (b'cpp', 'CPP tests')])),
                ('task', models.ForeignKey(to='tasks.Task')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IgnoringCBuilder',
            fields=[
                ('cbuilder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='checker.CBuilder')),
            ],
            options={
                'abstract': False,
            },
            bases=('checker.cbuilder',),
        ),
        migrations.CreateModel(
            name='IgnoringCBuilder2',
            fields=[
                ('cbuilder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='checker.CBuilder')),
            ],
            options={
                'abstract': False,
            },
            bases=('checker.cbuilder',),
        ),
        migrations.CreateModel(
            name='IgnoringCBuilder3',
            fields=[
                ('cbuilder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='checker.CBuilder')),
            ],
            options={
                'abstract': False,
            },
            bases=('checker.cbuilder',),
        ),
        migrations.CreateModel(
            name='IgnoringCXXBuilder',
            fields=[
                ('cxxbuilder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='checker.CXXBuilder')),
            ],
            options={
                'abstract': False,
            },
            bases=('checker.cxxbuilder',),
        ),
        migrations.CreateModel(
            name='IgnoringCXXBuilder2',
            fields=[
                ('cxxbuilder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='checker.CXXBuilder')),
            ],
            options={
                'abstract': False,
            },
            bases=('checker.cxxbuilder',),
        ),
        migrations.CreateModel(
            name='IgnoringCXXBuilder3',
            fields=[
                ('cxxbuilder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='checker.CXXBuilder')),
            ],
            options={
                'abstract': False,
            },
            bases=('checker.cxxbuilder',),
        ),
        migrations.RemoveField(
            model_name='cbuilder',
            name='_libs',
        ),
        migrations.RemoveField(
            model_name='cbuilder',
            name='_main_required',
        ),
        migrations.RemoveField(
            model_name='cxxbuilder',
            name='_libs',
        ),
        migrations.RemoveField(
            model_name='cxxbuilder',
            name='_main_required',
        ),
        migrations.AddField(
            model_name='cbuilder',
            name='_search_path',
            field=models.CharField(default=b'', help_text='flags for additional search path for compiler or linker ', max_length=1000, blank=True),
        ),
        migrations.AddField(
            model_name='cxxbuilder',
            name='_search_path',
            field=models.CharField(default=b'', help_text='flags for additional search path for compiler or linker ', max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='cbuilder',
            name='_file_pattern',
            field=models.CharField(default=b'^[a-zA-Z0-9_]*$', help_text='Regular expression describing all source files to be passed to the compiler or linker. (Play with  RegEx at <a href="http://pythex.org/" target="_blank">http://pythex.org/ </a>', max_length=1000),
        ),
        migrations.AlterField(
            model_name='cbuilder',
            name='_flags',
            field=models.CharField(default=b'-Wall -Wextra', help_text='Compiler or Linker flags', max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='cbuilder',
            name='_output_flags',
            field=models.CharField(default=b'-c -g -O0', help_text="Output flags. '%s' will be replaced by the program name.", max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='cxxbuilder',
            name='_file_pattern',
            field=models.CharField(default=b'^[a-zA-Z0-9_]*$', help_text='Regular expression describing all source files to be passed to the compiler or linker. (Play with  RegEx at <a href="http://pythex.org/" target="_blank">http://pythex.org/ </a>', max_length=1000),
        ),
        migrations.AlterField(
            model_name='cxxbuilder',
            name='_flags',
            field=models.CharField(default=b'-Wall -Wextra', help_text='Compiler or Linker flags', max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='cxxbuilder',
            name='_output_flags',
            field=models.CharField(default=b'-c -g -O0', help_text="Output flags. '%s' will be replaced by the program name.", max_length=1000, blank=True),
        ),
    ]

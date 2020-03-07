# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import checker.basemodels

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_jplag_up_to_date'),
        ('checker', '0004_textchecker_and_scalabuilder'),
    ]

    operations = [
        migrations.CreateModel(
            name='CLinker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('_main_required', models.BooleanField(default=True, help_text='Is a submission required to provide a main method or function?')),
                ('_libs', models.CharField(blank=True, default='', help_text="flags for libraries like '-lm ' as math library for C", max_length=1000)),
                ('_search_path', models.CharField(blank=True, default='', help_text='flags for additional search path for compiler or linker ', max_length=1000)),
                ('_flags', models.CharField(blank=True, default='-Wall -Wextra', help_text='Compiler or Linker flags', max_length=1000)),
                ('_file_pattern', models.CharField(default='^[a-zA-Z0-9_]*$', help_text='Regular expression describing all source files to be passed to the compiler or linker. (Play with  RegEx at <a href="http://pythex.org/" target="_blank">http://pythex.org/ </a>', max_length=1000)),
                ('_output_flags', models.CharField(choices=[('out', '-o %s (Link to executable program)'), ('so', '-shared -fPIC -o %s (Link to shared object)')], default='-o %s', help_text="choose link output type. '%s' will replaced by output_name. ", max_length=16)),
                ('_output_name', models.CharField(default='%s', help_text="choose a outputname. '%s' will be replaced by an internal default name.", max_length=16)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.Task')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CUnitChecker2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('file', checker.basemodels.CheckerFileField(help_text='The file that is copied into the sandbox', max_length=500, upload_to=checker.basemodels.get_checkerfile_storage_path)),
                ('filename', models.CharField(blank=True, help_text='What the file will be named in the sandbox. If empty, we try to guess the right filename!', max_length=500)),
                ('path', models.CharField(blank=True, help_text='Subfolder in the sandbox which shall contain the file.', max_length=500)),
                ('unpack_zipfile', models.BooleanField(default=False, help_text='Unpack the zip file into the given subfolder. (It will be an error if the file is not a zip file; the filename is ignored.)')),
                ('_test_name', models.CharField(default='TestApp.out', help_text='The fully qualified name of the test case executable (with fileending like .exe or .out)', max_length=100, verbose_name='TestApp Filename')),
                ('_test_ignore', models.CharField(blank=True, default="sorry, this feature doesn't work now", help_text='Regular Expression for ignoring files while compile and link test-code. <br> Play with  RegEx at <a href="http://pythex.org/" target="_blank">http://pythex.org/ </a>', max_length=4096)),
                ('_test_flags', models.CharField(blank=True, default='-Wall -Wextra -Wl,--warn-common', help_text="Compiler and Linker flags for i.e. libraries used while generating TestApp. <br> Don't fill in cunit or cppunit here.", max_length=1000)),
                ('link_type', models.CharField(choices=[('o', 'Link Trainers Test-Code with solution objects (*.o)'), ('so', 'MUT: Link solution objects as shared object (*.so, *.dll)'), ('out', 'MUT: Link solution objects as seperate executable program (*.out, *.exe)')], default='o', help_text='How to use solution submission in test-code?', max_length=16)),
                ('cunit_version', models.CharField(choices=[('cunit', 'CUnit 2.1-3'), ('cppunit', 'CppUnit 1.12.1'), ('c', 'C tests'), ('cpp', 'CPP tests')], default='cunit', max_length=16, verbose_name='Unittest type or library')),
                ('_test_par', models.CharField(blank=True, default='', help_text='Command line parameters for running TestApp', max_length=1000)),
                ('test_description', models.TextField(help_text='Description of the Testcase. To be displayed on Checker Results page when checker is  unfolded.')),
                ('name', models.CharField(help_text='Name of the Testcase. To be displayed as title on Checker Results page', max_length=100)),
                ('_sol_name', models.CharField(default='Solution', help_text='Basisfilename ( = filename without fileending!) for interaction with  MUT (Module-Under-Test)<br>The fileending to use gets determined by your choosen Link type.<br>', max_length=100, verbose_name='MUT Filename')),
                ('_sol_ignore', models.CharField(blank=True, default="sorry, this feature doesn't work now", help_text='Regular Expression for ignoring files while compile CUT and link MUT.<br>CUT = Code Under Test - MUT = Module Under Test <br>Play with RegEx at <a href="http://pythex.org/" target="_blank">http://pythex.org/ </a>', max_length=4096, verbose_name='MUT ignore files')),
                ('_sol_flags', models.CharField(blank=True, default='-Wall -Wextra -Wl,--warn-common', help_text='Compiler and Linker flags used while generating MUT (Module-under-Test).', max_length=1000, verbose_name='MUT flags')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.Task')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IgnoringCBuilder2',
            fields=[
                ('cbuilder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='checker.CBuilder')),
            ],
            options={
                'abstract': False,
            },
            bases=('checker.cbuilder',),
        ),
        migrations.CreateModel(
            name='IgnoringCXXBuilder2',
            fields=[
                ('cxxbuilder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='checker.CXXBuilder')),
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
            field=models.CharField(blank=True, default='', help_text='flags for additional search path for compiler or linker ', max_length=1000),
        ),
        migrations.AddField(
            model_name='cxxbuilder',
            name='_search_path',
            field=models.CharField(blank=True, default='', help_text='flags for additional search path for compiler or linker ', max_length=1000),
        ),
        migrations.AlterField(
            model_name='cbuilder',
            name='_file_pattern',
            field=models.CharField(default='^[a-zA-Z0-9_]*$', help_text='Regular expression describing all source files to be passed to the compiler or linker. (Play with  RegEx at <a href="http://pythex.org/" target="_blank">http://pythex.org/ </a>', max_length=1000),
        ),
        migrations.AlterField(
            model_name='cbuilder',
            name='_flags',
            field=models.CharField(blank=True, default='-Wall -Wextra', help_text='Compiler or Linker flags', max_length=1000),
        ),
        migrations.AlterField(
            model_name='cbuilder',
            name='_output_flags',
            field=models.CharField(blank=True, default='-c -g -O0', help_text="Output flags. '%s' will be replaced by the program name.", max_length=1000),
        ),
        migrations.AlterField(
            model_name='cxxbuilder',
            name='_file_pattern',
            field=models.CharField(default='^[a-zA-Z0-9_]*$', help_text='Regular expression describing all source files to be passed to the compiler or linker. (Play with  RegEx at <a href="http://pythex.org/" target="_blank">http://pythex.org/ </a>', max_length=1000),
        ),
        migrations.AlterField(
            model_name='cxxbuilder',
            name='_flags',
            field=models.CharField(blank=True, default='-Wall -Wextra', help_text='Compiler or Linker flags', max_length=1000),
        ),
        migrations.AlterField(
            model_name='cxxbuilder',
            name='_output_flags',
            field=models.CharField(blank=True, default='-c -g -O0', help_text="Output flags. '%s' will be replaced by the program name.", max_length=1000),
        ),
    ]

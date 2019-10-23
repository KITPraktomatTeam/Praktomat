# -*- coding: utf-8 -*-


from django.db import migrations, models
import checker.checker.DejaGnu
import checker.basemodels


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymityChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CBuilder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('_flags', models.CharField(default='-Wall', help_text='Compiler flags', max_length=1000, blank=True)),
                ('_output_flags', models.CharField(default='-o %s', help_text="Output flags. '%s' will be replaced by the program name.", max_length=1000, blank=True)),
                ('_libs', models.CharField(default='', help_text='Compiler libraries', max_length=1000, blank=True)),
                ('_file_pattern', models.CharField(default='^[a-zA-Z0-9_]*$', help_text='Regular expression describing all source files to be passed to the compiler.', max_length=1000)),
                ('_main_required', models.BooleanField(default=True, help_text='Is a submission required to provide a main method?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CheckerResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('passed', models.BooleanField(default=True, help_text='Indicates whether the test has been passed')),
                ('log', models.TextField(help_text='Text result of the checker')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('runtime', models.IntegerField(default=0, help_text='Runtime in milliseconds')),
            ],
        ),
        migrations.CreateModel(
            name='CheckerResultArtefact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=128)),
                ('file', models.FileField(help_text='Artefact produced by a checker', max_length=500, upload_to=checker.basemodels.get_checkerresultartefact_upload_path)),
            ],
        ),
        migrations.CreateModel(
            name='CheckStyleChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('name', models.CharField(default='CheckStyle', help_text='Name to be displayed on the solution detail page.', max_length=100)),
                ('configuration', checker.basemodels.CheckerFileField(help_text='XML configuration of CheckStyle. See http://checkstyle.sourceforge.net/', max_length=500, upload_to=checker.basemodels.get_checkerfile_storage_path)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CreateFileChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('file', checker.basemodels.CheckerFileField(help_text='The file that is copied into the sandbox', max_length=500, upload_to=checker.basemodels.get_checkerfile_storage_path)),
                ('filename', models.CharField(help_text='What the file will be named in the sandbox. If empty, we try to guess the right filename!', max_length=500, blank=True)),
                ('path', models.CharField(help_text='Subfolder in the sandbox which shall contain the file.', max_length=500, blank=True)),
                ('unpack_zipfile', models.BooleanField(default=False, help_text='Unpack the zip file into the given subfolder. (It will be an error if the file is not a zip file; the filename is ignored.)')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CXXBuilder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('_flags', models.CharField(default='-Wall', help_text='Compiler flags', max_length=1000, blank=True)),
                ('_output_flags', models.CharField(default='-o %s', help_text="Output flags. '%s' will be replaced by the program name.", max_length=1000, blank=True)),
                ('_libs', models.CharField(default='', help_text='Compiler libraries', max_length=1000, blank=True)),
                ('_file_pattern', models.CharField(default='^[a-zA-Z0-9_]*$', help_text='Regular expression describing all source files to be passed to the compiler.', max_length=1000)),
                ('_main_required', models.BooleanField(default=True, help_text='Is a submission required to provide a main method?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DejaGnuSetup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('test_defs', checker.basemodels.CheckerFileField(help_text='Das Setup benutzt den <A HREF="http://www.gnu.org/software/dejagnu/dejagnu.html">DejaGnu-Testrahmen</A>, um die Programme zu testen. Die in dieser Datei enthaltenen Definitionen gelten f\xfcr alle Testf\xe4lle dieser Aufgabe. Sie werden beim Testen in die DejaGnu-Datei <TT>default.exp</TT> geschrieben. (Vergl. hierzuden Abschnitt <EM>Target dependent procedures</EM> im\t<A HREF="http://www.gnu.org/manual/dejagnu/" TARGET="_blank">DejaGnu-Handbuch</A>.) Die Variablen PROGRAM und JAVA werden mit dem Programmnamen bzw. dem Pfad zur Java-Runtime ersetzt.', max_length=500, upload_to=checker.basemodels.get_checkerfile_storage_path)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, checker.checker.DejaGnu.DejaGnu),
        ),
        migrations.CreateModel(
            name='DejaGnuTester',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('name', models.CharField(help_text='The name of the Test', max_length=100)),
                ('test_case', checker.basemodels.CheckerFileField(help_text='In den folgenden DejaGnu-Testf\xe4llen werden typischerweise Funktionen aufgerufen, die beim vorherigen Schritt <EM>Tests einrichten</EM> definiert wurden.\t Siehe\tauch den Abschnitt <EM>How to write a test case</EM> im <A TARGET="_blank" HREF="http://www.gnu.org/manual/dejagnu/">DejaGnu-Handbuch</A>.', max_length=500, upload_to=checker.basemodels.get_checkerfile_storage_path)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, checker.checker.DejaGnu.DejaGnu),
        ),
        migrations.CreateModel(
            name='FortranBuilder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('_flags', models.CharField(default='-Wall', help_text='Compiler flags', max_length=1000, blank=True)),
                ('_output_flags', models.CharField(default='-o %s', help_text="Output flags. '%s' will be replaced by the program name.", max_length=1000, blank=True)),
                ('_libs', models.CharField(default='', help_text='Compiler libraries', max_length=1000, blank=True)),
                ('_file_pattern', models.CharField(default='^[a-zA-Z0-9_]*$', help_text='Regular expression describing all source files to be passed to the compiler.', max_length=1000)),
                ('_main_required', models.BooleanField(default=True, help_text='Is a submission required to provide a main method?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HaskellBuilder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('_flags', models.CharField(default='-Wall', help_text='Compiler flags', max_length=1000, blank=True)),
                ('_output_flags', models.CharField(default='-o %s', help_text="Output flags. '%s' will be replaced by the program name.", max_length=1000, blank=True)),
                ('_libs', models.CharField(default='', help_text='Compiler libraries', max_length=1000, blank=True)),
                ('_file_pattern', models.CharField(default='^[a-zA-Z0-9_]*$', help_text='Regular expression describing all source files to be passed to the compiler.', max_length=1000)),
                ('_main_required', models.BooleanField(default=True, help_text='Is a submission required to provide a main method?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HaskellTestFrameWorkChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('file', checker.basemodels.CheckerFileField(help_text='The file that is copied into the sandbox', max_length=500, upload_to=checker.basemodels.get_checkerfile_storage_path)),
                ('filename', models.CharField(help_text='What the file will be named in the sandbox. If empty, we try to guess the right filename!', max_length=500, blank=True)),
                ('path', models.CharField(help_text='Subfolder in the sandbox which shall contain the file.', max_length=500, blank=True)),
                ('unpack_zipfile', models.BooleanField(default=False, help_text='Unpack the zip file into the given subfolder. (It will be an error if the file is not a zip file; the filename is ignored.)')),
                ('test_description', models.TextField(help_text='Description of the Testcase. To be displayed on Checker Results page when checker is unfolded.')),
                ('name', models.CharField(help_text='Name of the Testcase. To be displayed as title on Checker Results page', max_length=100)),
                ('ignore', models.CharField(default='', help_text='space-seperated list of files to be ignored during compilation', max_length=4096, blank=True)),
                ('require_safe', models.BooleanField(default=True, help_text='Is a submission required to be Safe (according to GHCs Safe-Mode)?')),
                ('include_testcase_in_report', models.CharField(default='DL', help_text='Make the cestcases source available via the checkers result report?', max_length=4, choices=[(b'DL', b'Download-Link only'), (b'NO', b'Do not make the testcases source available'), (b'FULL', b'Also copy the source into the report')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterfaceChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('interface1', models.CharField(help_text='The name of the interface that must be implemeted.', max_length=100)),
                ('interface2', models.CharField(help_text='The name of the interface that must be implemeted.', max_length=100, blank=True)),
                ('interface3', models.CharField(help_text='The name of the interface that must be implemeted.', max_length=100, blank=True)),
                ('interface4', models.CharField(help_text='The name of the interface that must be implemeted.', max_length=100, blank=True)),
                ('interface5', models.CharField(help_text='The name of the interface that must be implemeted.', max_length=100, blank=True)),
                ('interface6', models.CharField(help_text='The name of the interface that must be implemeted.', max_length=100, blank=True)),
                ('interface7', models.CharField(help_text='The name of the interface that must be implemeted.', max_length=100, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IsabelleChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('logic', models.CharField(default='HOL', help_text='Default heap to use', max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JavaBuilder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('_flags', models.CharField(default='-Wall', help_text='Compiler flags', max_length=1000, blank=True)),
                ('_output_flags', models.CharField(default='-o %s', help_text="Output flags. '%s' will be replaced by the program name.", max_length=1000, blank=True)),
                ('_libs', models.CharField(default='', help_text='Compiler libraries', max_length=1000, blank=True)),
                ('_file_pattern', models.CharField(default='^[a-zA-Z0-9_]*$', help_text='Regular expression describing all source files to be passed to the compiler.', max_length=1000)),
                ('_main_required', models.BooleanField(default=True, help_text='Is a submission required to provide a main method?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JavaGCCBuilder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('_flags', models.CharField(default='-Wall', help_text='Compiler flags', max_length=1000, blank=True)),
                ('_output_flags', models.CharField(default='-o %s', help_text="Output flags. '%s' will be replaced by the program name.", max_length=1000, blank=True)),
                ('_libs', models.CharField(default='', help_text='Compiler libraries', max_length=1000, blank=True)),
                ('_file_pattern', models.CharField(default='^[a-zA-Z0-9_]*$', help_text='Regular expression describing all source files to be passed to the compiler.', max_length=1000)),
                ('_main_required', models.BooleanField(default=True, help_text='Is a submission required to provide a main method?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JUnitChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('class_name', models.CharField(help_text='The fully qualified name of the test case class (without .class)', max_length=100)),
                ('test_description', models.TextField(help_text='Description of the Testcase. To be displayed on Checker Results page when checker is  unfolded.')),
                ('name', models.CharField(help_text='Name of the Testcase. To be displayed as title on Checker Results page', max_length=100)),
                ('ignore', models.CharField(default='', help_text='space-seperated list of files to be ignored during compilation', max_length=4096)),
                ('junit_version', models.CharField(default='junit3', max_length=16, choices=[('junit4', 'JUnit 4'), ('junit3', 'JUnit 3')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KeepFileChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('filename', models.CharField(help_text='The name of the file to preserve (e.g. out.txt)', max_length=500, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LineCounter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LineWidthChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('max_line_length', models.IntegerField(default=80, help_text='The maximum length of a line of code.')),
                ('tab_width', models.IntegerField(default=4, help_text='The amount of characters a tab represents.')),
                ('include', models.CharField(default='.*', help_text='Regular expression describing the filenames to be checked. Case Insensetive. Blank: use all files.', max_length=100, blank=True)),
                ('exclude', models.CharField(default='.*\\.txt$', help_text='Regular expression describing included filenames, which shall be excluded. Case Insensetive. Blank: use all files.', max_length=100, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('r_script', models.CharField(help_text='R script to execute. If left blank, it will run any *.R file, as long as there is only one.', max_length=100, blank=True)),
                ('require_plots', models.BooleanField(default=False, help_text='Require the script to create an Rplots.pdf file.')),
                ('keep_plots', models.BooleanField(default=True, help_text='If the R script creates a Rplots.pdf file, keep it.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScriptChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('name', models.CharField(default='Externen Tutor ausführen', help_text='Name to be displayed on the solution detail page.', max_length=100)),
                ('shell_script', checker.basemodels.CheckerFileField(help_text='A script (e.g. a shell script) to run. Its output will be displayed to the user (if public), the checker will succeed if it returns an exit code of 0. The environment will contain the variables JAVA and PROGRAM.', max_length=500, upload_to=checker.basemodels.get_checkerfile_storage_path)),
                ('remove', models.CharField(help_text='Regular expression describing passages to be removed from the output.', max_length=5000, blank=True)),
                ('returns_html', models.BooleanField(default=False, help_text="If the script doesn't return HTML it will be enclosed in &lt; pre &gt; tags.")),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TextChecker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('order', models.IntegerField(help_text='Determines the order in wich the checker will start. Not necessary continuously!')),
                ('public', models.BooleanField(default=True, help_text='Test results are displayed to the submitter.')),
                ('required', models.BooleanField(default=False, help_text='The test must be passed to submit the solution.')),
                ('always', models.BooleanField(default=True, help_text='The test will run on submission time.')),
                ('critical', models.BooleanField(default=False, help_text='If this test fails, do not display further test results.')),
                ('text', models.TextField(help_text='The text that has to be in the solution.')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IgnoringHaskellBuilder',
            fields=[
                ('haskellbuilder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='checker.HaskellBuilder', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('checker.haskellbuilder',),
        ),
        migrations.CreateModel(
            name='IgnoringJavaBuilder',
            fields=[
                ('javabuilder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='checker.JavaBuilder', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('checker.javabuilder',),
        ),
        migrations.CreateModel(
            name='TestOnlyBuildingBuilder',
            fields=[
                ('haskellbuilder_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='checker.HaskellBuilder', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('checker.haskellbuilder',),
        ),
    ]

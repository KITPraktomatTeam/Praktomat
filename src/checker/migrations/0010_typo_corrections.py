from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0009_isabelle_checker_trusted_to_additional_theories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymitychecker',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='cbuilder',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='checkstylechecker',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='createfilechecker',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='cxxbuilder',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='dejagnusetup',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='dejagnutester',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='fortranbuilder',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='haskellbuilder',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='haskelltestframeworkchecker',
            name='ignore',
            field=models.CharField(default='', help_text='space-separated list of files to be ignored during compilation', max_length=4096, blank=True),
        ),
        migrations.AlterField(
            model_name='haskelltestframeworkchecker',
            name='include_testcase_in_report',
            field=models.CharField(default='DL', help_text='Make the testcases source available via the checkers result report?', max_length=4, choices=[(b'DL', b'Download-Link only'), (b'NO', b'Do not make the testcases source available'), (b'FULL', b'Also copy the source into the report')]),
        ),
        migrations.AlterField(
            model_name='haskelltestframeworkchecker',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='interfacechecker',
            name='interface1',
            field=models.CharField(help_text='The name of the interface that must be implemented.', max_length=100),
        ),
        migrations.AlterField(
            model_name='interfacechecker',
            name='interface2',
            field=models.CharField(help_text='The name of the interface that must be implemented.', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='interfacechecker',
            name='interface3',
            field=models.CharField(help_text='The name of the interface that must be implemented.', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='interfacechecker',
            name='interface4',
            field=models.CharField(help_text='The name of the interface that must be implemented.', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='interfacechecker',
            name='interface5',
            field=models.CharField(help_text='The name of the interface that must be implemented.', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='interfacechecker',
            name='interface6',
            field=models.CharField(help_text='The name of the interface that must be implemented.', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='interfacechecker',
            name='interface7',
            field=models.CharField(help_text='The name of the interface that must be implemented.', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='interfacechecker',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='isabellechecker',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='javabuilder',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='javagccbuilder',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='junitchecker',
            name='ignore',
            field=models.CharField(default='', help_text='space-separated list of files to be ignored during compilation, i.e.: these files will not be compiled.', max_length=4096, blank=True),
        ),
        migrations.AlterField(
            model_name='junitchecker',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='junitchecker',
            name='test_description',
            field=models.TextField(help_text='Description of the Testcase. To be displayed on Checker Results page when checker is unfolded.'),
        ),
        migrations.AlterField(
            model_name='keepfilechecker',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='linecounter',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='linewidthchecker',
            name='exclude',
            field=models.CharField(default='.*\\.txt$', help_text='Regular expression describing included filenames, which shall be excluded. Case insensitive. Blank: use all files.', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='linewidthchecker',
            name='include',
            field=models.CharField(default='.*', help_text='Regular expression describing the filenames to be checked. Case insensitive. Blank: use all files.', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='linewidthchecker',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='rchecker',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='scalabuilder',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='scriptchecker',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
        migrations.AlterField(
            model_name='textchecker',
            name='order',
            field=models.IntegerField(help_text='Determines the order in which the checker will start. Not necessary continuously!'),
        ),
    ]

# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0007_auto_20170429_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='junitchecker',
            name='ignore',
            field=models.CharField(default='', help_text='space-seperated list of files to be ignored during compilation, i.e.: these files will not be compiled.', max_length=4096, blank=True),
        ),
        migrations.AlterField(
            model_name='scriptchecker',
            name='filename',
            field=models.CharField(help_text='What the file will be named in the sandbox. If empty, we try to guess the right filename!', max_length=500, blank=True),
        ),
    ]

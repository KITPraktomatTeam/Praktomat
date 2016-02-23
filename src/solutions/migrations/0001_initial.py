# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import solutions.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(help_text='Id unique in task and user.Eg. Solution 1 of user X in task Y in contrast to global solution Z', editable=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('testupload', models.BooleanField(default=False, help_text='Indicates whether this solution is a test upload by a trainer or tutor.')),
                ('accepted', models.BooleanField(default=False, help_text='Indicates whether the solution has passed all public and required tests.')),
                ('warnings', models.BooleanField(default=False, help_text='Indicates whether the solution has at least failed one public and not required tests.')),
                ('plagiarism', models.BooleanField(default=False, help_text='Indicates whether the solution is a rip-off of another one.')),
                ('final', models.BooleanField(default=False, help_text='Indicates whether this solution is the last (accepted) of the author.')),
                ('author', models.ForeignKey(verbose_name=b'solution author', to='accounts.User')),
            ],
        ),
        migrations.CreateModel(
            name='SolutionFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(help_text='Source code file as part of a solution an archive file (.zip, .tar or .tar.gz) containing multiple solution files.', max_length=500, upload_to=solutions.models.get_solutionfile_upload_path)),
                ('mime_type', models.CharField(help_text='Guessed file type. Automatically  set on save().', max_length=100)),
                ('solution', models.ForeignKey(to='solutions.Solution')),
            ],
        ),
    ]

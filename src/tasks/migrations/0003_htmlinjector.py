# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tasks.models
import utilities.deleting_file_field


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_jplag_up_to_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='HtmlInjector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inject_in_solution_view', models.BooleanField(default=False, help_text='Indicates whether HTML code shall be injected in public  solution views, e.g.: in https://praktomat.cs.kit.edu/2016_WS_Abschluss/solutions/5710/')),
                ('inject_in_solution_full_view', models.BooleanField(default=False, help_text='Indicates whether HTML code shall be injected in private solution views, e.g.: in https://praktomat.cs.kit.edu/2016_WS_Abschluss/solutions/5710/full')),
                ('inject_in_attestation_edit', models.BooleanField(default=True, help_text='Indicates whether HTML code shall be injected in attestation edits, e.g.: in https://praktomat.cs.kit.edu/2016_WS_Abschluss/attestation/134/edit')),
                ('inject_in_attestation_view', models.BooleanField(default=False, help_text='Indicates whether HTML code shall be injected in attestation views, e.g.: in https://praktomat.cs.kit.edu/2016_WS_Abschluss/attestation/134')),
                ('html_file', utilities.deleting_file_field.DeletingFileField(max_length=500, upload_to=tasks.models.get_htmlinjectorfile_storage_path)),
                ('task', models.ForeignKey(to='tasks.Task')),
            ],
        ),
    ]

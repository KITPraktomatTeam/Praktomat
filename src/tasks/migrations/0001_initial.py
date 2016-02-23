# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tasks.models
import utilities.deleting_file_field


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0001_initial'),
        ('attestation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('media_file', utilities.deleting_file_field.DeletingFileField(max_length=500, upload_to=tasks.models.get_mediafile_storage_path)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='The name of the Task', max_length=100)),
                ('description', models.TextField(help_text='Description of the assignment.')),
                ('publication_date', models.DateTimeField(help_text='The time on which the user will see the task.')),
                ('submission_date', models.DateTimeField(help_text='The time up until the user has time to complete the task. This time will be extended by one hour for those who yust missed the deadline.')),
                ('supported_file_types', models.CharField(default=b'^(text/.*|image/.*|application/pdf)$', help_text='Regular Expression describing the mime types of solution files that the user is allowed to upload.', max_length=1000)),
                ('max_file_size', models.IntegerField(default=1000, help_text='The maximum size of an uploaded solution file in kilobyte.')),
                ('all_checker_finished', models.BooleanField(default=False, help_text="Indicates whether the checker which don't run immediately on submission have been executed.", editable=False)),
                ('only_trainers_publish', models.BooleanField(default=False, help_text='Indicates that only trainers may publish attestations. Otherwise, tutors may publish final attestations within their tutorials.')),
                ('final_grade_rating_scale', models.ForeignKey(to='attestation.RatingScale', help_text='The scale used to mark the whole solution.', null=True)),
                ('model_solution', models.ForeignKey(related_name='model_solution_task', blank=True, to='solutions.Solution', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='mediafile',
            name='task',
            field=models.ForeignKey(to='tasks.Task'),
        ),
    ]

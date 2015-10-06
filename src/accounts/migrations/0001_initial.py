# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.auth.models
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name of the tutorial', max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('mat_number', models.IntegerField(blank=True, null=True, validators=[accounts.models.validate_mat_number])),
                ('final_grade', models.CharField(help_text='The final grade for the whole class.', max_length=100, null=True, blank=True)),
                ('programme', models.CharField(help_text='The programme the student is enlisted in.', max_length=100, null=True, blank=True)),
                ('activation_key', models.CharField(verbose_name='activation key', max_length=40, editable=False)),
                ('tutorial', models.ForeignKey(blank=True, to='accounts.Tutorial', help_text='The tutorial the student belongs to.', null=True)),
            ],
            options={
                'ordering': ['first_name', 'last_name'],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='tutorial',
            name='tutors',
            field=models.ManyToManyField(help_text='The tutors in charge of the tutorium.', related_name='tutored_tutorials', to='accounts.User'),
        ),
    ]

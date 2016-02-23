# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chunk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(help_text=b'A unique name for this chunk of content', unique=True, max_length=255, editable=False)),
                ('content', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_validation_regex', models.CharField(default=b'.*@(student.)?kit.edu', help_text=b'Regular expression used to check the email domain of registering users.', max_length=200, blank=True)),
                ('mat_number_validation_regex', models.CharField(default=b'\\d{5,7}', help_text=b'Regular expression used to check the student number.', max_length=200, blank=True)),
                ('new_users_via_sso', models.BooleanField(default=True, help_text=b'If enabled, users previously unknown to the Praktomat can register via sigle sign on (eg. Shibboleth).')),
                ('deny_registration_from', models.DateTimeField(default=datetime.date(2222, 1, 1), help_text=b'After this date, registration wont be possible.')),
                ('acount_activation_days', models.IntegerField(default=10, help_text=b'Days until the user has time to activate his account with the link send in the registation email.')),
                ('account_manual_validation', models.BooleanField(default=False, help_text=b'If enabled, registrations via the website must be manually validate by a trainer.')),
                ('accept_all_solutions', models.BooleanField(default=False, help_text=b'If enabled, solutions with required checkers, which are not passed, can become the final soution.')),
                ('anonymous_attestation', models.BooleanField(default=False, help_text=b"If enabled, the tutor can't see the name of the user, who subbmitted the solution.")),
                ('final_grades_published', models.BooleanField(default=False, help_text=b'If enabeld, all users can see their final grades.')),
                ('invisible_attestor', models.BooleanField(default=False, help_text=b'If enabeld, users will not learn which tutor wrote attestations to his solutions. In particular, tutors will not ne named in Attestation-Emails.')),
                ('attestation_reply_to', models.EmailField(help_text=b'Addiotional Reply-To: Address to be set for Attestation emails.', max_length=254, blank=True)),
            ],
            options={
                'verbose_name': 'Setting',
            },
        ),
        migrations.AddField(
            model_name='chunk',
            name='settings',
            field=models.ForeignKey(default=1, to='configuration.Settings', help_text=b'Makes it easy to display chunks as inlines in Settings.'),
        ),
    ]

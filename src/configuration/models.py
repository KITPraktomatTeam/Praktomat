# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from datetime import date, timedelta

class Settings(models.Model):
    """ Singleton object containing site wide settings configurable by the trainer. """

    class Meta:
        # Django admin adds an 's' to the class name; prevent SettingSS
        verbose_name = 'Setting'

    email_validation_regex = \
            models.CharField(
                max_length=200,
                blank=True,
                default=".*@(student.)?kit.edu",
                help_text="Regular expression used to check the email domain of registering users."
            )

    mat_number_validation_regex = \
            models.CharField(
                max_length=200,
                blank=True,
                default="\d{5,7}",
                help_text="Regular expression used to check the student number."
            )

    new_users_via_sso = \
            models.BooleanField(
                default=True,
                help_text="If enabled, users previously unknown to the Praktomat can register via single sign on (eg. Shibboleth)."
            )

    deny_registration_from = \
            models.DateTimeField(
                default=date(2222, 1, 1),
                help_text="After this date, registration won't be possible."
            )

    acount_activation_days = \
            models.IntegerField(
                default=10,
                help_text="Days until the user has time to activate his account with the link sent in the registration email."
            )

    account_manual_validation = \
            models.BooleanField(
                default=False,
                help_text="If enabled, registrations via the website must be manually validated by a trainer."
            )

    requires_disclaimer_acceptance = \
            models.BooleanField(
                default=False,
                help_text="If enabled, users have to accept the disclaimer before using the site."
            )

    accept_all_solutions = \
            models.BooleanField(
                default=False,
                help_text="If enabled, solutions can become the final solution even if not all required checkers are passed."
            )

    anonymous_attestation = \
            models.BooleanField(
                default=False,
                help_text="If enabled, the tutor can't see the name of the user who submitted the solution."
            )

    final_grades_published = \
            models.BooleanField(
                default=False,
                help_text="If enabled, all users can see their final grades."
            )

    SUM = 'SUM'
    AVERAGE = 'AVG'

    ARITHMETIC_CHOICES = (
        (SUM, 'Sum'),
        (AVERAGE, 'Average'),
    )

    final_grades_arithmetic_option = \
            models.CharField(
                max_length=3,
                choices=ARITHMETIC_CHOICES,
                default=SUM,
            )

    WITH_PLAGIARISM = 'WP'
    NO_PLAGIARISM = 'NP'

    PLAGIARISM_CHOICES = (
        (NO_PLAGIARISM, 'Without'),
        (WITH_PLAGIARISM, 'Including'),
    )

    final_grades_plagiarism_option = \
            models.CharField(
                max_length=2,
                choices=PLAGIARISM_CHOICES,
                default=NO_PLAGIARISM,
            )

    invisible_attestor = \
            models.BooleanField(
                default=False,
                help_text="If enabled, a user will not learn which tutor wrote attestations to his solutions. In particular, tutors will not be named in attestation emails."
            )

    attestation_reply_to = \
            models.EmailField(
                blank=True,
                help_text="Additional Reply-To: address to be set for attestation emails."
            )

    attestation_allow_run_checkers = \
            models.BooleanField(
                default=False,
                help_text="If enabled, tutors can re-run all checkers for solutions they attest. Can be used to re-run checks that failed due to problems unrelated to the solution (e.g.: time-outs because of high server load), but needs to be used with care, since it may change the results from what the student saw when he submitted his solution."
            )

    jplag_setting = \
            models.CharField(
                max_length=200,
                default='Java',
                help_text="Default settings for jPlag"
            )

    hide_solutions_of_expired_tasks = \
            models.BooleanField(
                default=False,
                help_text="If enabled, solutions (incl. attestations) of expired tasks are not accessible for students."
            )

    deadline_tolerance = \
            models.DurationField(
                default=timedelta(hours=1),
                help_text="The duration by which the submission date for a task will be extended for those who just missed the deadline."
            )

    tutors_can_edit_solutions = \
            models.BooleanField(
                default=False,
                help_text="If enabled, tutors can also upload solutions for students in their tutorial."
            )

@python_2_unicode_compatible
class Chunk(models.Model):
    """ A Chunk is a piece of content associated with a unique key that can be inserted into any template with the use of a special template tag """
    settings = models.ForeignKey(
            Settings,
            default=1,
            help_text="Makes it easy to display chunks as inlines in Settings.",
            on_delete=models.CASCADE
        )

    key = \
            models.CharField(
                help_text="A unique name for this chunk of content",
                blank=False,
                max_length=255,
                unique=True,
                editable=False
            )

    content = models.TextField(blank=True)

    def __str__(self):
        return "%s" % (self.key,)

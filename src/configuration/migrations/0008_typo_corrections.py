from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0007_settings_final_grades_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='accept_all_solutions',
            field=models.BooleanField(default=False, help_text=b'If enabled, solutions can become the final solution even if not all required checkers are passed.'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='account_manual_validation',
            field=models.BooleanField(default=False, help_text=b'If enabled, registrations via the website must be manually validated by a trainer.'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='acount_activation_days',
            field=models.IntegerField(default=10, help_text=b'Days until the user has time to activate his account with the link sent in the registration email.'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='anonymous_attestation',
            field=models.BooleanField(default=False, help_text=b"If enabled, the tutor can't see the name of the user who submitted the solution."),
        ),
        migrations.AlterField(
            model_name='settings',
            name='attestation_allow_run_checkers',
            field=models.BooleanField(default=False, help_text=b'If enabled, tutors can re-run all checkers for solutions they attest. Can be used to re-run checks that failed due to problems unrelated to the solution (e.g.: time-outs because of high server load), but needs to be used with care, since it may change the results from what the student saw when he submitted his solution.'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='attestation_reply_to',
            field=models.EmailField(help_text=b'Additional Reply-To: address to be set for attestation emails.', max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='settings',
            name='deny_registration_from',
            field=models.DateTimeField(default=datetime.date(2222, 1, 1), help_text=b"After this date, registration won't be possible."),
        ),
        migrations.AlterField(
            model_name='settings',
            name='final_grades_published',
            field=models.BooleanField(default=False, help_text=b'If enabled, all users can see their final grades.'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='invisible_attestor',
            field=models.BooleanField(default=False, help_text=b'If enabled, a user will not learn which tutor wrote attestations to his solutions. In particular, tutors will not be named in attestation emails.'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='new_users_via_sso',
            field=models.BooleanField(default=True, help_text=b'If enabled, users previously unknown to the Praktomat can register via single sign on (eg. Shibboleth).'),
        ),
    ]

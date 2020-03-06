# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0002_initial_configuration'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='attestation_allow_run_checkers',
            field=models.BooleanField(default=False, help_text=b'If enabled, tutors can re-run all checkers for solutions they attest. Can be used to re-run checks that failed due to problems unrelated to the solutione (e.g.: time-outs because of high server-load), but needs to be used with care, since it may change the results from what the student saw when he submitted his solution.'),
        ),
    ]

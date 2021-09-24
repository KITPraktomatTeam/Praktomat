# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0003_settings_attestation_allow_run_checkers'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='jplag_setting',
            field=models.CharField(default='Java', help_text=b'Default settings for jPlag', max_length=200),
        ),
    ]

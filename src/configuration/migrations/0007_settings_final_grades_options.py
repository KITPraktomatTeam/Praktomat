# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0006_settings_warning_message_chunk'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='final_grades_arithmetic_option',
            field=models.CharField(default='SUM', max_length=3, choices=[('SUM', 'Sum'), ('AVG', 'Average')]),
        ),
        migrations.AddField(
            model_name='settings',
            name='final_grades_plagiarism_option',
            field=models.CharField(default='NP', max_length=2, choices=[('NP', 'Without'), ('WP', 'Including')]),
        ),
    ]

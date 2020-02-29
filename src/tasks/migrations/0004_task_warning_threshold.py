# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_htmlinjector'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='warning_threshold',
            field=models.DecimalField(default=0, help_text='If the student has less points in his tasks than the sum of their warning thresholds, display a warning.', max_digits=8, decimal_places=2),
        ),
    ]

# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0002_solution_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='testupload',
            field=models.BooleanField(default=False, help_text='Indicates whether this solution is a test upload.'),
        ),
    ]

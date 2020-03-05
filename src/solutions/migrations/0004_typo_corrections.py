from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0003_auto_20151120_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='number',
            field=models.IntegerField(help_text='Id unique in task and user. E.g. Solution 1 of user X in task Y in contrast to global solution Z', editable=False),
        ),
        migrations.AlterField(
            model_name='solution',
            name='warnings',
            field=models.BooleanField(default=False, help_text='Indicates whether the solution has at least failed one public and not required test.'),
        ),
    ]

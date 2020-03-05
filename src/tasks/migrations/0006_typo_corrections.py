from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_task_ordering'),
    ]

    operations = [
        migrations.AlterField(
            model_name='htmlinjector',
            name='inject_in_solution_view',
            field=models.BooleanField(default=False, help_text='Indicates whether HTML code shall be injected in public solution views, e.g.: in https://praktomat.cs.kit.edu/2016_WS_Abschluss/solutions/5710/'),
        ),
        migrations.AlterField(
            model_name='task',
            name='submission_date',
            field=models.DateTimeField(help_text='The time up until the user has time to complete the task. This time will be extended by one hour for those who just missed the deadline.'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(help_text='The name of the task', max_length=100),
        ),
    ]

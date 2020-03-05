from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_add_coordinator_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='tutors',
            field=models.ManyToManyField(help_text='The tutors in charge of the tutorial.', related_name='tutored_tutorials', to='accounts.User'),
        ),
    ]

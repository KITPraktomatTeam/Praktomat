from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_Task_dynamic_upload_waiting_time_Python3_Python2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='max_file_size',
            field=models.IntegerField(default=1000, help_text='The maximum size of an uploaded solution file in kibibyte.'),
        ),
    ]

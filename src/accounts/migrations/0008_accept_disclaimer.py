# Generated by Django 2.2.11 on 2020-04-15 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_custom_user_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='accepted_disclaimer',
            field=models.BooleanField(default=False, help_text='Whether the user accepted the disclaimer.'),
        ),
    ]

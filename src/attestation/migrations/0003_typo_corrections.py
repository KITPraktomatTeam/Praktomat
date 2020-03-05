from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attestation', '0002_auto_20151006_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratingaspect',
            name='name',
            field=models.CharField(help_text='The Name of the Aspect to be rated. E.g.: "Readability"', max_length=100),
        ),
    ]

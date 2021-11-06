# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnnotatedSolutionFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(help_text='The content of the solution file annotated by the tutor.', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attestation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('public_comment', models.TextField(help_text='Comment which is shown to the user.', blank=True)),
                ('private_comment', models.TextField(help_text='Comment which is only visible to tutors', blank=True)),
                ('final', models.BooleanField(default=False, help_text='Indicates whether the attestation is ready to be published')),
                ('published', models.BooleanField(default=False, help_text='Indicates whether the user can see the attestation.')),
                ('published_on', models.DateTimeField(help_text='The Date/Time the attestation was published.', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='RatingAspect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The Name of the Aspect to be rated. E.g.: "Readabylity"', max_length=100)),
                ('description', models.TextField(help_text='Description of the Aspect and how it should be rated. E.w.: "How well is the code structured?"')),
            ],
        ),
        migrations.CreateModel(
            name='RatingResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attestation', models.ForeignKey(to='attestation.Attestation', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='RatingScale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The Name of the rating scale for the aspects. E.g.: "School marks"', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RatingScaleItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The Name of the item(mark) in the rating scale. E.g.: "A" or "very good" ', max_length=100)),
                ('position', models.PositiveSmallIntegerField(help_text='Defines the order in which the items are sorted. Lowest is best.')),
                ('scale', models.ForeignKey(to='attestation.RatingScale', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('script', models.TextField(default='var sum = 0.0;\nfor (x = 0; x != grades.length; ++x) {\n    grade = parseFloat(grades[x]);\n    if (!isNaN(grade)) {\n        sum += grade;\n    }\n}\nresult=sum;', help_text='This JavaScript will calculate a recommend end note for every user based on final grade of every task.', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='ratingresult',
            name='mark',
            field=models.ForeignKey(to='attestation.RatingScaleItem', null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='ratingresult',
            name='rating',
            field=models.ForeignKey(to='attestation.Rating', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='rating',
            name='aspect',
            field=models.ForeignKey(to='attestation.RatingAspect', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='rating',
            name='scale',
            field=models.ForeignKey(to='attestation.RatingScale', on_delete=models.CASCADE),
        ),
    ]

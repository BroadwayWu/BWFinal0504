# Generated by Django 2.0.1 on 2018-01-24 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_survey_outcome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey_outcome',
            name='Question6',
            field=models.CharField(max_length=200),
        ),
    ]

# Generated by Django 2.0.4 on 2018-04-20 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_userrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='PicSave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(upload_to='upload/')),
            ],
        ),
    ]
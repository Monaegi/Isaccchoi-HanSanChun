# Generated by Django 2.0.1 on 2018-01-29 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20180129_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weightworkout',
            name='thumbnail',
        ),
        migrations.AddField(
            model_name='weightworkout',
            name='image',
            field=models.ImageField(blank=True, upload_to='thumbnail'),
        ),
    ]

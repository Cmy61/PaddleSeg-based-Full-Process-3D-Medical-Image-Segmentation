# Generated by Django 3.2.5 on 2023-04-13 06:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20230410_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='volume',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='ctset',
            name='build_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 13, 6, 20, 33, 632960, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='build_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 13, 6, 20, 33, 629959, tzinfo=utc)),
        ),
    ]
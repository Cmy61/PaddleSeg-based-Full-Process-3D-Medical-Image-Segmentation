# Generated by Django 3.2.5 on 2023-04-10 14:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20230410_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctset',
            name='build_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 10, 22, 12, 39, 828780)),
        ),
        migrations.AlterField(
            model_name='project',
            name='build_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 10, 22, 12, 39, 827773)),
        ),
    ]

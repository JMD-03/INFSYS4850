# Generated by Django 3.1.2 on 2020-10-29 18:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('times', '0007_auto_20201029_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timekeep',
            name='in_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 29, 18, 28, 10, 512576, tzinfo=utc)),
        ),
    ]
# Generated by Django 3.1.2 on 2020-11-14 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='end_Time',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='start_Time',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
    ]

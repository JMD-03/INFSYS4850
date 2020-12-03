# Generated by Django 3.1.2 on 2020-11-20 05:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_auto_20201119_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='PTO_Hours',
            field=models.FloatField(default=0, max_length=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(200)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='Sick_Hours',
            field=models.FloatField(default=0, max_length=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(200)]),
        ),
    ]
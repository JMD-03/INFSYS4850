# Generated by Django 3.1.2 on 2020-12-02 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_auto_20201119_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='request_Type',
            field=models.TextField(choices=[('Paid Time Off', 'Paid Time Off'), ('Sick Day', 'Sick Day'), ('Overtime', 'Overtime'), ('Time Correction', 'Time Correction')], default='Paid Time Off'),
        ),
    ]

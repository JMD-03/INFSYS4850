# Generated by Django 3.1.2 on 2020-11-14 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20201113_2118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='user_id',
            new_name='user',
        ),
    ]

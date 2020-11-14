# Generated by Django 3.1.2 on 2020-11-14 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RightsSupport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('employee_view', 'Global Employee View'), ('supervisor_view', 'Global supervisor view'), ('management_view', 'Global management view')),
                'managed': False,
                'default_permissions': (),
            },
        ),
    ]

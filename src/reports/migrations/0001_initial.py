<<<<<<< HEAD
# Generated by Django 3.1.2 on 2020-11-10 00:34

from django.db import migrations, models
=======
# Generated by Django 3.1.2 on 2020-11-10 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
>>>>>>> Sahil


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
=======
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
>>>>>>> Sahil
    ]

    operations = [
        migrations.CreateModel(
            name='RightsSupport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
<<<<<<< HEAD
                'managed': False,
            },
        ),
=======
                'permissions': (('employee_view', 'Global Employee View'), ('supervisor_view', 'Global supervisor view'), ('management_view', 'Global management view')),
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='reportModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
>>>>>>> Sahil
    ]

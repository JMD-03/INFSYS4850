# Generated by Django 3.1.2 on 2020-11-14 03:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('PTO_Hours', models.FloatField(default=0)),
                ('Sick_Hours', models.FloatField(default=0)),
                ('PTO_Accrual_Rate', models.FloatField(default=0)),
                ('Sick_Accrual_Rate', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_Type', models.TextField(choices=[('Paid Time Off Request', 'Paid Time Off'), ('Sick Day Request', 'Sick Day'), ('Overtime Request', 'Overtime'), ('Time Correction Request', 'Time Correction')], default='Paid Time Off Request')),
                ('start_Date', models.DateField(default=None)),
                ('end_Date', models.DateField(default=None)),
                ('start_Time', models.TimeField(blank=True, default=None)),
                ('end_Time', models.TimeField(blank=True, default=None)),
                ('status', models.TextField(choices=[('Requested', 'Requested'), ('Approved', 'Approved'), ('Denied', 'Denied')], default='Requested')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

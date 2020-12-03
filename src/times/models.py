from django.db import models
from django.contrib.auth.models import User
from datetime import date, time
import datetime
from django.utils import timezone


# Create your models here.

class timeKeep(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class timeType(models.TextChoices):
		Paid_Time_Off = 'Paid Time Off'
		Sick_Day = 'Sick Time'
		Overtime = 'Overtime'
		Standardtime = 'Standard Time'
		

	timeType = models.TextField(
		choices=timeType.choices,
		default=timeType.Standardtime
    )

	in_time = models.DateTimeField(blank = True, null = True)	
	
	lunchin_time = models.DateTimeField(blank = True, null = True)

	lunchout_time = models.DateTimeField(blank = True, null = True)

	out_time = models.DateTimeField(blank = True, null = True)

	clocked_in = models.BooleanField(default = False)
	
	is_Manual = models.BooleanField(default = False)

	week_number = models.IntegerField(default = timezone.now().isocalendar().week)

	dateTimeEntered = models.DateTimeField(default = None, null = True)
	#class Meta:
	#	constraints = [models.UniqueConstraint(fields=['user', 'dateTimeEntered'], name='unique user date')]

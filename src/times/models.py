from django.db import models
from django.contrib.auth.models import User
from datetime import date, time
from django.utils import timezone
import datetime


# Create your models here.

class timeKeep(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	in_time = models.DateTimeField(blank = True, null = True)	
	
	lunchin_time = models.DateTimeField(blank = True, null = True)

	lunchout_time = models.DateTimeField(blank = True, null = True)

	out_time = models.DateTimeField(blank = True, null = True)

	clocked_in = models.BooleanField(default = False)

	currentDate = models.DateField(default = datetime.date.today)
	class Meta:
		constraints = [models.UniqueConstraint(fields=['user', 'currentDate'], name='unique user date')]

		

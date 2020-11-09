from django.db import models
from django.contrib.auth.models import User
from datetime import date, time
from django.utils import timezone
from datetime import datetime


# Create your models here.

class timeKeep(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	in_time = models.DateTimeField(blank = True, null = True)	
	
	lunchin_time = models.DateTimeField(blank = True, null = True)

	lunchout_time = models.DateTimeField(blank = True, null = True)

	out_time = models.DateTimeField(blank = True, null = True)

	clocked_in = models.BooleanField(default = True)

	def __str__(self):
		return str(self.user)

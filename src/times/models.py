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

	def __str__(self):
		return str(self.user)
	
	def save(self):
		time = timeKeep
		date = timezone.now()
		time.objects.filter(in_time__date = date)
		if self.id is not None:
			self.id = time.id
		super().save()
		

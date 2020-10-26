from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class timeKeep(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	in_time = models.DateTimeField(default = timezone.now)
	
	lunch_timein = models.DateTimeField(null = True, blank = True)

	lunch_timeout = models.DateTimeField(null = True, blank = True)

	out_time = models.DateTimeField(null = True, blank = True)

	clocked_in = models.BooleanField(default = True)

	def clock_in(self):
		self.clocked_in = True
		self.save()

	def lunch_in(self):
		self.lunch_timein = timezone.now()
		self.clocked_in = False
		self.save()

	def lunch_out(self):
		self.lunch_timeout = timezone.now()
		self.clocked_in = True
		self.save()

	def clock_out(self):
		self.out_time = timezone.now()
		self.clocked_in = False
		self.save()
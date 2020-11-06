from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class timeKeep(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)

	in_time = models.DateTimeField(blank = True, null = True)	

	out_time = models.DateTimeField(blank = True, null = True)

	lunchin_time = models.DateTimeField(blank = True, null = True)

	lunchout_time = models.DateTimeField(blank = True, null = True)

	clocked_in = models.BooleanField(default = True)
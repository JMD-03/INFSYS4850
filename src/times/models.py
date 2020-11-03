from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class timeKeep(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	in_time = models.DateTimeField(default = timezone.now())	
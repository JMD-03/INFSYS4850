from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


class time(models.Model):
   # clockIN = models.DateTimeField(default=datetime.today())
   # clockOUT = models.DateTimeField(default=datetime.today())
    manualEntry = models.BooleanField(default=False)
    date = models.DateTimeField()

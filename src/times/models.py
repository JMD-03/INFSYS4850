from django.db import models
from django.contrib.auth.models import User
from datetime import date, time

# Create your models here.
class time(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    #date = models.DateField(default=date())
    #clockIN = models.TimeField(default=dat)
    manualEntry = models.BooleanField(default=False)
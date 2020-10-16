from django.db import models

# Create your models here.
class time(models.Model):
    user = models.TextField(blank=True) #This will actually be blank=false
    date = models.DateTimeField(blank=True) #will actually be blank=false
    manualEntry = models.BooleanField(default=False)

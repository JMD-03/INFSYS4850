from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    PTO_Hours = models.FloatField(default=0)
    Sick_Hours = models.FloatField(default=0)
    PTO_Accrual_Rate = models.FloatField(default=0)
    Sick_Accrual_Rate = models.FloatField(default=0)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userAttribute(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        primary_key=True
    )
    PTO_Hours = models.FloatField(default=0)
    Sick_Hours = models.FloatField(default=0)
    PTO_Accrual_Rate = models.FloatField(default=0)
    Sick_Accrual_Rate = models.FloatField(default=0)

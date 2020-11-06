from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import datetime

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    PTO_Hours = models.FloatField(default=0)
    Sick_Hours = models.FloatField(default=0)
    PTO_Accrual_Rate = models.FloatField(default=0)
    Sick_Accrual_Rate = models.FloatField(default=0)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Request_Type(models.TextChoices):
        Paid_Time_Off = 'Paid Time Off Request'
        Sick_Day = 'Sick Day Request'
        Overtime = 'Overtime Request'
        Time_Correction = "Time Correction Request"

    request_Type = models.TextField(
        choices=Request_Type.choices,
        default=Request_Type.Paid_Time_Off
    )
    # start_Date = models.DateField(default=None)
    # end_Date = models.DateField(default=None)
    # start_Time = models.TimeField(default=None)
    # end_Time = models.TimeField(default=None)
    start_Date_Time = models.DateTimeField(default=None)
    end_Date_Time = models.DateTimeField(default=None)

    class cur_Status(models.TextChoices):
        requested = 'Requested'
        approved = 'Approved'
        denied = 'Denied'

    status = models.TextField(
        choices=cur_Status.choices,
        default=cur_Status.requested
    )

    def __str__(self):
        return self.user.first_name + " " + self.request_Type

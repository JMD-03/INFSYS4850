from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models import signals


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    PTO_Hours = models.FloatField(default=0, max_length=3, validators=[MinValueValidator(0), MaxValueValidator(200)])
    Sick_Hours = models.FloatField(default=0, max_length=3, validators=[MinValueValidator(0), MaxValueValidator(200)])
    PTO_Accrual_Rate = models.FloatField(default=0, max_length=3)
    Sick_Accrual_Rate = models.FloatField(default=0, max_length=3)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def save(self, *args, **kwargs):
        
        try:
            prof = self.user.id
            prof = Profile.objects.get(user=prof)
            print(prof.PTO_Hours)
            print(self.PTO_Hours)
            if self.PTO_Hours == prof.PTO_Hours:
                pass #do nothing
            else:
                if self.PTO_Hours % 1 != 0:
                    x = self.PTO_Hours % 1
                    self.PTO_Hours = (((self.PTO_Hours//1)*60) + (x * 60))
                else:
                    self.PTO_Hours *= 60

            if self.PTO_Accrual_Rate == prof.PTO_Accrual_Rate:
                pass #do nothing
            else:
                if self.PTO_Accrual_Rate % 1 != 0:
                    x = self.PTO_Accrual_Rate % 1
                    self.PTO_Accrual_Rate = (((self.PTO_Accrual_Rate//1)*60) + (x * 60))
                else:
                    self.PTO_Accrual_Rate *= 60

            if self.Sick_Hours == prof.Sick_Hours:
                pass  # do nothing
            else:
                if self.Sick_Hours % 1 != 0:
                    x = self.Sick_Hours % 1
                    self.Sick_Hours = (((self.Sick_Hours//1)*60) + (x * 60))
                else:
                    self.Sick_Hours *= 60

            if self.Sick_Accrual_Rate == prof.Sick_Accrual_Rate:
                pass  # do nothing
            else:
                if self.Sick_Accrual_Rate % 1 != 0:
                    x = self.Sick_Accrual_Rate % 1
                    self.Sick_Accrual_Rate = (((self.Sick_Accrual_Rate//1)*60) + (x * 60))
                else:
                    self.Sick_Accrual_Rate *= 60
        except:
            if self.PTO_Accrual_Rate % 1 != 0:
                x = self.PTO_Accrual_Rate % 1
                self.PTO_Accrual_Rate = (((self.PTO_Accrual_Rate//1)*60) + (x * 60))
            else:
                self.PTO_Accrual_Rate *= 60
            if self.Sick_Accrual_Rate % 1 != 0:
                x = self.Sick_Accrual_Rate % 1
                self.Sick_Accrual_Rate = (((self.Sick_Accrual_Rate//1)*60) + (x * 60))
            else:
                self.Sick_Accrual_Rate *= 60
            if self.PTO_Hours % 1 != 0:
                x = self.PTO_Hours % 1
                self.PTO_Hours = (((self.PTO_Hours//1)*60) + (x * 60))
            else:
                self.PTO_Hours *= 60
            if self.Sick_Hours % 1 != 0:
                x = self.Sick_Hours % 1
                self.Sick_Hours = (((self.Sick_Hours//1)*60) + (x * 60))
            else:
                self.Sick_Hours *= 60

        super(Profile, self).save(*args, **kwargs)

# This deletes the user if the profile is deleted.
# def delete_user(sender, instance=None, **kwargs):
#     try:
#         instance.user
#         print(instance.user)
#     except User.DoesNotExist:
#         pass
#     else:
#         instance.user.delete()
#         print(instance.user)
# signals.post_delete.connect(delete_user, sender=Profile)



class Request(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
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

    def save(self, *args, **kwargs):
        try:
            status = self.status
            if status == "Requested":
                print("status requested")
                pass #Do Nothing
            elif status == "Approved":
                print("Status approved")
                #call stored procedure, can pass user, request type, and start/end time
            else:
                print("status denied")
                pass #Do nothing for now with denied requests
        except:
            print("in except")
        super(Request, self).save(*args, **kwargs)

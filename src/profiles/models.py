from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import datetime, timedelta, now
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError
from django.db import connection
from django.shortcuts import render, HttpResponse
from times.models import timeKeep


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    PTO_Hours = models.FloatField(default=0, max_length=3, validators=[MinValueValidator(0), MaxValueValidator(200)])
    Sick_Hours = models.FloatField(default=0, max_length=3, validators=[MinValueValidator(0), MaxValueValidator(200)])
    PTO_Accrual_Rate = models.FloatField(default=0, max_length=3, validators=[MinValueValidator(0), MaxValueValidator(200)])
    Sick_Accrual_Rate = models.FloatField(default=0, max_length=3,  validators=[MinValueValidator(0), MaxValueValidator(200)])

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def save(self, *args, **kwargs):

        try:
            prof = self.user.id
            prof = Profile.objects.get(user=prof)
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


class Request(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Request_Type(models.TextChoices):
        Paid_Time_Off = 'Paid Time Off'
        Sick_Day = 'Sick Day'
        Overtime = 'Overtime'
        Time_Correction = "Time Correction"

    request_Type = models.TextField(
        choices=Request_Type.choices,
        default=Request_Type.Paid_Time_Off
    )

    submission_Date = models.DateTimeField(default=timezone.now())

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

    def clean(self, *args, **kwargs):
        req_type = self.request_Type
        start_date_time = self.start_Date_Time
        end_date_time = self.end_Date_Time
        if ((self.status == "Approved") and (req_type == "Paid Time Off" or req_type == "Sick Day")):
            prof = self.user.id
            prof = Profile.objects.get(user=prof)
            if req_type == "Paid Time Off":
                shours = prof.PTO_Hours
                if start_date_time < now():
                    raise ValidationError("You can't submit this request for a day in the past.")
            elif req_type == "Sick Day":
                shours = prof.Sick_Hours
            if (self.end_Date_Time < self.start_Date_Time):
                raise ValidationError("End date should be greater than start date.")
            if (self.start_Date_Time == self.end_Date_Time):
                raise ValidationError("Start and end time can not match.")
            calc_time = end_date_time - start_date_time
            seconds = calc_time.total_seconds()
            minutes = seconds // 60
            remain_time = (minutes % 60) // 60
            old_req = now() - start_date_time
            if (start_date_time.weekday() >= 5):
                raise ValidationError("Your start or end date can not be a weekend.")
            if (end_date_time.weekday() >= 5):
                raise ValidationError("Your start or end date can not be a weekend.")
            if (end_date_time.hour + (end_date_time.minute/60)) - (start_date_time.hour + (start_date_time.minute/60)) > 8:
                raise ValidationError("The start and end times of this request are more than 8 hours apart. You can't have over 8 hours between the starting and ending times (the hours and minutes fields).")
            if (end_date_time.hour + (end_date_time.minute/60)) == (start_date_time.hour + (start_date_time.minute/60)):
                raise ValidationError("You can't input the same start and end hours for a request. (ex. you can't request Dec. 2 8am - Dec 3. 8am. Request Dec 2. 8am-4pm instead.)")
            if (calc_time.days == 0 and start_date_time.day == end_date_time.day):         # Check if this is a single day request
                day = start_date_time + timedelta(days=calc_time.days)
                if (day.weekday() < 5):
                    if (minutes/60) > 8:
                        raise ValidationError("You can not request over 8 hours of time for a single day.")
                    elif (minutes + remain_time < 60):
                        raise ValidationError("Minimum request time is one hour.")
                    elif (shours < minutes):
                        raise ValidationError("You do not have enough banked time to cover this request 1.")
                else:
                    raise ValidationError("Your are submitting a single day request for a weekend")

            elif (calc_time.days == 0 and start_date_time.day != end_date_time.day):
                raise ValidationError("Please check your timing. You have entered a multiple day request with less than 24 hours separating the entries.")
            elif ((start_date_time.minute not in [0,15,30,45]) or (end_date_time.minute not in [0,15,30,45])):
                raise ValidationError("Your start and end time must utilize 15 minute increments(0,15,30,45).")
            elif (end_date_time.hour > 23):
                raise ValidationError("Start and end times for this request must be between 5am and 11pm.")
            elif (start_date_time.hour < 5 or start_date_time.hour > 23):
                raise ValidationError("Start and end times for this request must be between 5am and 11pm.")
            else:
                total_days = 0
                if (end_date_time.hour + (end_date_time.minute/60)) - (start_date_time.hour + (start_date_time.minute/60)) != 8:
                    raise ValidationError("For multi day requests you must put exactly 8 hours between the starting hours/minutes and the ending hours/minutes. (ex. 8am-4pm). If you are attempting to take a partial day with full days on the front or back of the request please use two requests. One for the partial day, and another for the full days.")
                for i in range(calc_time.days + 1):
                    day = start_date_time + timedelta(days=i)
                    if (day.weekday() >= 5):
                        pass
                    else:
                        total_days += 1
                        minutes = ((total_days * 8) * 60)
                if shours < minutes:
                    raise ValidationError("You don't have enough time banked to cover this request.")
                elif minutes == 0:
                    raise ValidationError("You've managed to put in a request for only a weekend. That's not valid! Please add some weekdays to this request.")

        elif self.status == "Approved" and req_type == "Overtime":
            if (end_date_time.hour + (end_date_time.minute/60)) - (start_date_time.hour + (start_date_time.minute/60)) > 8:
                raise ValidationError("The start and end times of this request are more than 8 hours apart. You can't have over 8 hours between the starting and ending times (the hours and minutes fields).")
            if ((start_date_time.day != end_date_time.day) or (start_date_time.month != end_date_time.month) or (start_date_time.year != end_date_time.year)):
                raise ValidationError("You can not enter an overtime request with different start and end dates")

        elif req_type == "Time Correction" and self.status == "Approved":
            if (end_date_time.hour + (end_date_time.minute/60)) - (start_date_time.hour + (start_date_time.minute/60)) > 8:
                raise ValidationError("The start and end times of this request are more than 8 hours apart. You can't have over 8 hours between the starting and ending times (the hours and minutes fields).")
            if start_date_time > now():
                raise ValidationError("You can't correct a future time.")
            if ((start_date_time.day != end_date_time.day) or (start_date_time.month != end_date_time.month) or (start_date_time.year != end_date_time.year)):
                raise ValidationError("A time correction request must be put in for only a single day")


    def save(self, *args, **kwargs):
        status = self.status
        if status == "Requested":
            pass #Do Nothing
        elif status == "Approved":
            req_type = self.request_Type
            start_date_time = self.start_Date_Time
            end_date_time = self.end_Date_Time
            if req_type == "Overtime":
                total_days = 0
            if req_type == "Paid Time Off" or req_type == "Sick Day":
                prof = self.user.id
                prof = Profile.objects.get(user=prof)
                calc_time = end_date_time - start_date_time

            with connection.cursor() as cursor:
                try:
                    if req_type == "Paid Time Off" or req_type == "Sick Day":
                        minutes = 0
                    hours_add = timedelta(hours=6)
                    in_time = self.start_Date_Time + hours_add
                    out_time = self.end_Date_Time + hours_add
                    cur_user = self.user_id

                    if req_type != "Time Correction":
                        if len(str(in_time.day)) == 1:
                            x = ("0" + str(in_time.day))
                            setDate = (str(in_time.year) + "-" + str(in_time.month) + "-" + x)
                        else:
                            setDate = (str(in_time.year) + "-" + str(in_time.month) + "-" + str(in_time.day))
                        if start_date_time.day == end_date_time.day:
                            cursor.execute("INSERT into times_timekeep (in_time,lunchin_time,lunchout_time,out_time,clocked_in,user_id,timetype,dateTimeEntered, is_Manual) VALUES(%s, NULL, NULL, %s, 0, %s, %s, %s, 0)", [in_time, out_time, cur_user, req_type,setDate])
                            if req_type == "Paid Time Off" or req_type == "Sick Day":
                                minutes += ((end_date_time.hour*60)+end_date_time.minute) - ((start_date_time.hour*60) + start_date_time.minute)
                        else:
                            for i in range(calc_time.days + 1):
                                day = start_date_time + timedelta(days=i)
                                if day.weekday() >= 5:
                                    pass
                                else:
                                    in_time = day
                                    in_time = in_time + hours_add
                                    out_time = day
                                    if out_time.day != end_date_time.day:
                                        x = timedelta(hours=8)
                                        out_time += x
                                    else:
                                        out_time = end_date_time
                                    minutes += ((out_time.hour*60)+out_time.minute) - ((start_date_time.hour*60) + start_date_time.minute)
                                    out_time = out_time + hours_add
                                    cursor.execute("INSERT into times_timekeep (in_time,lunchin_time,lunchout_time,out_time,clocked_in,user_id,timetype,dateTimeEntered, is_Manual) VALUES(%s, NULL, NULL, %s, 0, %s, %s, %s, 0)", [in_time, out_time, cur_user, req_type,setDate])

                    else:  #req type does equal time correction so it can only be a single day.
                        if len(str(in_time.day)) == 1:
                            x = ("0" + str(in_time.day))
                            setDate = (str(in_time.year) + "-" + str(in_time.month) + "-" + x)
                        else:
                            setDate = (str(in_time.year) + "-" + str(in_time.month) + "-" + str(in_time.day))
                        timeType = "Standard Time"
                        times = timeKeep.objects.filter(user_id=cur_user, timeType="Standard Time", in_time__icontains=setDate)
                        if times.exists():
                            cursor.execute("UPDATE times_timekeep SET lunchin_time = NULL, lunchout_time = NULL, in_time = %s, out_time = %s, timeType = %s WHERE date(in_time) = date(%s) AND user_id = %s AND timeType = %s", [in_time, out_time, timeType, self.start_Date_Time, cur_user, timeType])
                        else:
                            cursor.execute("INSERT into times_timekeep (in_time,lunchin_time,lunchout_time,out_time,clocked_in,user_id,timetype,dateTimeEntered, is_Manual) VALUES(%s, NULL, NULL, %s, 0, %s, %s, %s, 0)", [in_time, out_time, cur_user, timeType,setDate])


                    if req_type == 'Paid Time Off':
                        new_hours = (prof.PTO_Hours - minutes)
                        cursor.execute("UPDATE profiles_profile SET PTO_Hours = %s WHERE user_id = %s", [new_hours,cur_user] )

                    elif req_type == 'Sick Day':
                        new_hours = (prof.Sick_Hours - minutes)
                        cursor.execute("UPDATE profiles_profile SET Sick_Hours = %s WHERE user_id = %s", [new_hours,cur_user] )

                except IntegrityError as e:
                    raise ValueError(e, " You violated the minimum or maximum value of a PTO or sick bank limit with this request.")
                    return HttpResponse("You violated the minimum or maximum value of a PTO or sick bank limit with this request.")
                finally:
                    cursor.close()



        else:
            pass #Do nothing for now with denied requests

        super(Request, self).save(*args, **kwargs)
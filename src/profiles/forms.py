from django import forms
from django.forms.widgets import DateTimeInput
from django.utils.timezone import datetime, timedelta, now
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Request
import logging


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username",
                  "email", "password1", "password2")


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('PTO_Hours',
                  'Sick_Hours',
                  'PTO_Accrual_Rate',
                  'Sick_Accrual_Rate',)


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class RequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RequestForm, self).__init__(*args, **kwargs)

    class Meta:
        widgets = {'start_Date_Time': DateTimeInput(format='%Y-%m-%d %H:%M'),   # widget creates html date picker combined with above datetimeinput class
                   'end_Date_Time':   DateTimeInput(format='%Y-%m-%d %H:%M'),}
        model = Request
        fields = ('request_Type', 'start_Date_Time', 'end_Date_Time')

    def clean(self):
        cleaned_data = super().clean()
        reqType = cleaned_data.get("request_Type")
        start_date_time = cleaned_data.get("start_Date_Time")
        end_date_time = cleaned_data.get("end_Date_Time")
        prof = self.user.id
        prof = Profile.objects.get(user=prof)
        calc_time = end_date_time - start_date_time
        seconds = calc_time.total_seconds()
        minutes = seconds // 60
        total_days = seconds // 86400                               # Number of full days the request involves
        remain_time = seconds % 86400
        old_req = now() - start_date_time                               # What is left over after number of full days

        if (end_date_time < start_date_time):
            raise forms.ValidationError("End date should be greater than start date.")
        if (start_date_time == end_date_time):
            raise forms.ValidationError("Start and end time can not match.")
        if (old_req.days > 14):
            raise forms.ValidationError("You can't submit a request for more than two weeks in the past. Please talk directly to management about this request.")

        if (reqType == "Paid Time Off Request"):
            pto = prof.PTO_Hours * 60                                       # Get PTO hours and convert to minutes for more accurate comparison
            print("total days: ", total_days)
            print("calc_time: ", calc_time.days)
            print("remain_time: ", remain_time)
            if (calc_time.days == 0 and start_date_time.day == end_date_time.day):         # Check if this is a single day request
                day = start_date_time + timedelta(days=calc_time.days)
                print(day)
                if (day.weekday() < 4):
                    if (minutes/60) > 8:                                       
                        raise forms.ValidationError("You can not request over 8 hours of PTO for a single day.")
                        if (remain_time < 3600):
                            raise forms.ValidationError("Minimum request time is one hour.")
                    if (pto < minutes):                                         
                        raise forms.ValidationError("You do not have enough PTO to cover this request 1.")
                else:
                    raise forms.ValidationError("Your are submitting a single day PTO request for a weekend")
            
            elif (calc_time.days == 0 and start_date_time.day != end_date_time.day):
                raise forms.ValidationError("Please check your timing. You have entered a multiple day request with less than 24 hours separating the entries.")

            elif (calc_time.days > 14):
                raise forms.ValidationError("PTO Requests must be put in at less than 14 day increments.") 
            else:
                total_days = 0
                print(calc_time.days)
                if calc_time.days == 1:
                    if remain_time == 0:
                        total_days += 1
                        print("added 1 to total days")
                        minutes = ((total_days * 8) * 60)
                    else:
                        total_days += 1
                        minutes = remain_time // 60
                        minutes += ((total_days * 8) * 60)
                        print("added 1 to total days in else")
                else:        
                    for i in range(calc_time.days):
                        day = start_date_time + timedelta(days=i)
                        print(day)
                        if (remain_time == 0):
                            if (day.weekday() < 4):
                                total_days += 1
                                print("ran if")
                        else:
                            if (day.weekday() < 4):
                                total_days += 1
                                minutes = remain_time // 60
                                print("ran else")
                    if (minutes != (seconds // 60)):
                        minutes += ((total_days * 8) * 60)
                        print("set minutes +=")
                    else:
                        minutes = ((total_days * 8) * 60)                             
                        print("set minutes in else")
                print("minutes ", minutes)
                print("pto time: ", pto)
                if (pto < minutes):                                     
                    raise forms.ValidationError("You do not have enough PTO to cover this request 2.")
                else:
                    if minutes == 0:
                        raise forms.ValidationError("You've submitted a request only for a weekend.")
                    else:
                        pass
                print("total time off: ", minutes)
            print("total time off: ", minutes)

        elif (reqType == "Sick Day Request"):
            sick = prof.Sick_Hours * 60                                       # Get sick hours and convert to minutes for more accurate comparison
            print("total days: ", total_days)
            print("calc_time: ", calc_time.days)
            print("remain_time: ", remain_time)
            if (calc_time.days == 0 and start_date_time.day == end_date_time.day):         # Check if this is a single day request
                day = start_date_time + timedelta(days=calc_time.days)
                print(day)
                if (day.weekday() < 4):
                    if (minutes/60) > 8:                                       
                        raise forms.ValidationError("You can not request over 8 hours of sick time for a single day.")
                        if (remain_time < 3600):
                            raise forms.ValidationError("Minimum request time is one hour.")
                    if (sick < minutes):                                         
                        raise forms.ValidationError("You do not have enough sick time to cover this request 1.")
                else:
                    raise forms.ValidationError("Your are submitting a single day sick request for a weekend")
            
            elif (calc_time.days == 0 and start_date_time.day != end_date_time.day):
                raise forms.ValidationError("Please check your timing. You have entered a multiple day request with less than 24 hours separating the entries.")

            elif (calc_time.days > 7):
                raise forms.ValidationError("Sick Day Requests must be put in at less than 8 day increments.") 
            else:
                total_days = 0
                print(calc_time.days)
                if calc_time.days == 1:
                    if remain_time == 0:
                        total_days += 1
                        print("added 1 to total days")
                        minutes = ((total_days * 8) * 60)
                    else:
                        total_days += 1
                        minutes = remain_time // 60
                        minutes += ((total_days * 8) * 60)
                        print("added 1 to total days in else")
                else:        
                    for i in range(calc_time.days):
                        day = start_date_time + timedelta(days=i)
                        print(day)
                        if (remain_time == 0):
                            if (day.weekday() < 4):
                                total_days += 1
                                print("ran if")
                        else:
                            if (day.weekday() < 4):
                                total_days += 1
                                minutes = remain_time // 60
                                print("ran else")
                    if (minutes != (seconds // 60)):
                        minutes += ((total_days * 8) * 60)
                        print("set minutes +=")
                    else:
                        minutes = ((total_days * 8) * 60)                             
                        print("set minutes in else")
                print("minutes ", minutes)
                print("pto time: ", pto)
                if (pto < minutes):                                     
                    raise forms.ValidationError("You do not have enough sick time to cover this request 2.")
                else:
                    if minutes == 0:
                        raise forms.ValidationError("You've submitted a request only for a weekend.")
                    else:
                        pass
                print("total time off: ", minutes)
            print("total time off: ", minutes)

        elif (reqType == "Overtime Request"):
            print("total days: ", total_days)
            print("calc_time: ", calc_time.days)
            print("remain_time: ", remain_time)
            if ((start_date_time.day != end_date_time.day) or (start_date_time.month != end_date_time.month) or (start_date_time.year != end_date_time.year)):
                raise forms.ValidationError("You can not enter an overtime request with different start and end dates")

        elif (reqType == "Time Correction Request"):
            print("total days: ", total_days)
            print("calc_time: ", calc_time.days)
            print("remain_time: ", remain_time)
            if ((start_date_time.day != end_date_time.day) or (start_date_time.month != end_date_time.month) or (start_date_time.year != end_date_time.year)):
                raise forms.ValidationError(
                    "A time correction request must be put in for only a single day")

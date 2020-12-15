from django import forms
from django.forms.widgets import DateTimeInput
from django.utils.timezone import datetime, timedelta, now
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Request


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username",
                  "email", "password1", "password2")

class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        PTO_Hours = self.instance.PTO_Hours
        Sick_Hours = self.instance.Sick_Hours
        PTO_Accrual_Rate = self.instance.PTO_Accrual_Rate
        Sick_Accrual_Rate = self.instance.Sick_Accrual_Rate
        if PTO_Hours % 60 != 0:
            x = PTO_Hours % 60
            PTO_Hours = ((PTO_Hours//60) + (x / 60))
        else:
            PTO_Hours //= 60

        if PTO_Accrual_Rate % 60 != 0:
            x = PTO_Accrual_Rate % 60
            PTO_Accrual_Rate = (
                (PTO_Accrual_Rate//60) + (x / 60))
        else:
            PTO_Accrual_Rate //= 60

        if Sick_Hours % 60 != 0:
            x = Sick_Hours % 60
            Sick_Hours = ((Sick_Hours//60) + (x / 60))
        else:
            Sick_Hours //= 60

        if Sick_Accrual_Rate % 60 != 0:
            x = Sick_Accrual_Rate % 60
            Sick_Accrual_Rate = (
                (Sick_Accrual_Rate//60) + (x / 60))
        else:
            Sick_Accrual_Rate //= 60

        self.initial['PTO_Hours'] = PTO_Hours
        self.initial['Sick_Hours'] = Sick_Hours
        self.initial['PTO_Accrual_Rate'] = PTO_Accrual_Rate
        self.initial['Sick_Accrual_Rate'] = Sick_Accrual_Rate


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

    def clean(self, *args, **kwargs):
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
        remain_time = (minutes % 60) // 60
        old_req = now() - start_date_time                               # What is left over after number of full days

        if (end_date_time < start_date_time):
            raise forms.ValidationError("End date should be greater than start date.")
        if (start_date_time == end_date_time):
            raise forms.ValidationError("Start and end time can not match.")
        if (old_req.days > 14):
            raise forms.ValidationError("You can't submit a request for more than two weeks in the past. Please talk directly to management about this request.")
        if (end_date_time.hour + (end_date_time.minute/60)) - (start_date_time.hour + (start_date_time.minute/60)) > 8:
            raise forms.ValidationError("The start and end times of this request are more than 8 hours apart. You can't have over 8 hours between the starting and ending times (the hours and minutes fields).")

        if (reqType == "Paid Time Off" or reqType == "Sick Day"):
            if reqType == "Paid Time Off":
                shours = prof.PTO_Hours
                if start_date_time < now():
                    raise forms.ValidationError("You can't submit this request for a day in the past.")
            elif reqType == "Sick Day":
                shours = prof.Sick_Hours
            if (start_date_time.weekday() >= 5):
                raise forms.ValidationError("Your start or end date can not be a weekend.")
            if (end_date_time.weekday() >= 5):
                raise forms.ValidationError("Your start or end date can not be a weekend.")
            if (calc_time.days == 0 and start_date_time.day == end_date_time.day):         # Check if this is a single day request
                day = start_date_time + timedelta(days=calc_time.days)
                if (day.weekday() < 5):
                    if (minutes/60) > 8:                                       
                        raise forms.ValidationError("You can not request over 8 hours of time for a single day.")
                    if (minutes + remain_time < 60):
                        raise forms.ValidationError("Minimum request time is one hour.")
                    if (shours < minutes):                                         
                        raise forms.ValidationError("You do not have enough banked time to cover this request 1.")
                else:
                    raise forms.ValidationError("Your are submitting a single day request for a weekend")
            
            elif (calc_time.days == 0 and start_date_time.day != end_date_time.day):
                raise forms.ValidationError("For multi day requests you must put exactly 8 hours between the starting hours/minutes and the ending hours/minutes. (ex. 8am-4pm). If you are attempting to take a partial day with full days on the front or back of the request please use two requests. One for the partial day, and another for the full days.")
            elif ((start_date_time.minute not in [0,15,30,45]) or (end_date_time.minute not in [0,15,30,45])):
                raise forms.ValidationError("Your start and end time must utilize 15 minute increments(0,15,30,45).")
            elif (end_date_time.hour > 23):
                raise forms.ValidationError("Start and end times for this request must be between 5am and 11pm.")
            elif (start_date_time.hour < 5 or start_date_time.hour > 23):
                raise forms.ValidationError("Start and end times for this request must be between 5am and 11pm.")
            else:
                total_days = 0
                if (end_date_time.hour + (end_date_time.minute/60)) - (start_date_time.hour + (start_date_time.minute/60)) != 8:
                    raise forms.ValidationError("For multi day requests you must put exactly 8 hours between the starting hours/minutes and the ending hours/minutes. (ex. 8am-4pm). If you are attempting to take a partial day with full days on the front or back of the request please use two requests. One for the partial day, and another for the full days.")
                for i in range(calc_time.days + 1):
                    day = start_date_time + timedelta(days=i)
                    if (day.weekday() >= 5):
                        pass
                    else:
                        total_days += 1
                        minutes = ((total_days * 8) * 60)
                if shours < minutes:
                    raise forms.ValidationError("You don't have enough time banked to cover this request.")
                elif minutes == 0:
                    raise forms.ValidationError("You've managed to put in a request for only a weekend. That's not valid! Please add some weekdays to this request.")

        elif reqType == "Overtime":
            if (end_date_time.hour + (end_date_time.minute/60)) - (start_date_time.hour + (start_date_time.minute/60)) > 8:
                raise forms.ValidationError("The start and end times of this request are more than 8 hours apart. You can't have over 8 hours between the starting and ending times (the hours and minutes fields).")
            if ((start_date_time.day != end_date_time.day) or (start_date_time.month != end_date_time.month) or (start_date_time.year != end_date_time.year)):
                raise forms.ValidationError("You can not enter an overtime request with different start and end dates")

        elif reqType == "Time Correction":
            if (end_date_time.hour + (end_date_time.minute/60)) - (start_date_time.hour + (start_date_time.minute/60)) > 8:
                raise forms.ValidationError("The start and end times of this request are more than 8 hours apart. You can't have over 8 hours between the starting and ending times (the hours and minutes fields).")
            if start_date_time > now():
                raise forms.ValidationError("You can't correct a future time.")
            if ((start_date_time.day != end_date_time.day) or (start_date_time.month != end_date_time.month) or (start_date_time.year != end_date_time.year)):
                raise forms.ValidationError("A time correction request must be put in for only a single day")
            
        else:
            raise forms.ValidationError("Unknown error while getting request type. Please relaunch this website and try again. If the issue repeats please contact management.")



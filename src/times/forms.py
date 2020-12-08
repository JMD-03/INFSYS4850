from django import forms
from django.forms.widgets import DateTimeInput
from django.forms import ModelForm
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import datetime, timedelta
from times.models import timeKeep

#input for widget
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

#form data
class timeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(timeForm, self).__init__(*args, **kwargs)

    class Meta: #used to create calander dropdown menus
        widgets = {'in_time': DateTimeInput(format='%Y-%m-%d %H:%M' ),
                   'lunchin_time': DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'lunchout_time': DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'out_time': DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'clocked_in': forms.HiddenInput(),
                   'is_Manual':forms.HiddenInput(),
                   'dateTimeEntered': forms.DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'user': forms.HiddenInput()
                   }

        model = timeKeep
        fields = ["in_time", "lunchin_time", "lunchout_time", "out_time", "clocked_in", "dateTimeEntered"]
        labels = {
            "lunchin_time": "Lunch start",
            "lunchout_time": "Lunch end"
        }
    
        #model function for manual time incase user goes out of bounds
    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("user")
        in_Time = cleaned_data.get("in_time")
        lunchin_Time = cleaned_data.get("lunchin_time")
        lunchout_Time = cleaned_data.get("lunchout_time")
        out_Time = cleaned_data.get("out_time")
        datetimeentered = cleaned_data.get("dateTimeEntered")
        #datetimeentered = datetimeentered - timedelta(hours = 6)
        try: 
            if user is None:
                if in_Time:
                    datetimeentered = in_Time.date()
                    #timekeep = timeKeep.objects.filter(user = self.user, timeType = "Standard Time").get(dateTimeEntered = datetimeentered.date())
                if lunchin_Time:
                    datetimeentered = lunchin_Time.date()
                    # timekeep = timeKeep.objects.filter(user = self.user, timeType = "Standard Time").get(dateTimeEntered = datetimeentered.date())
                if lunchout_Time:
                    datetimeentered = lunchout_Time.date()
                    #timekeep = timeKeep.objects.filter(user = self.user, timeType = "Standard Time").get(dateTimeEntered = datetimeentered.date())
                if out_Time:
                    datetimeentered = out_Time.date()
                    #timekeep = timeKeep.objects.filter(user = self.user, timeType = "Standard Time").get(dateTimeEntered = datetimeentered.date())
                timekeep = timeKeep.objects.filter(user = self.user, timeType = "Standard Time").get(dateTimeEntered = datetimeentered)
            else:
                timekeep = timeKeep.objects.filter(user = user, timeType = "Standard Time").get(dateTimeEntered = in_Time)
            if timekeep.in_time:
                in_Time2 = timekeep.in_time 
            if timekeep.lunchin_time:
                lunchin_Time2 = timekeep.lunchin_time
            if timekeep.lunchout_time: 
                lunchout_Time2 = timekeep.lunchout_time
        except:
            pass
        if out_Time:
            if user is None:
                timecheck(out_Time)
            if lunchout_Time  and out_Time < lunchout_Time:
                raise forms.ValidationError("Your clock out time should be greater than lunch clock out")
            if lunchin_Time  and out_Time < lunchin_Time:
                raise forms.ValidationError("Your clock out time should be greater than lunch clock in")
            if in_Time:
                if out_Time < in_Time:
                    raise forms.ValidationError("Your clock out time should be greater than clock in")
                if (out_Time - in_Time).total_seconds() > 29700:
                    raise forms.ValidationError("Cannot be clocked in over eight hours")
            if 'in_Time2' not in locals() and in_Time is None:
                raise forms.ValidationError("you cannot clock out without clocking in")
            if 'in_Time2' in locals(): 
                if out_Time < in_Time2:
                    raise forms.ValidationError("your clock out time should be greater than your saved clock in ")
                if (out_Time - in_Time2).total_seconds() > 29700:
                    raise forms.ValidationError("you cannot clock in over eight hours")
            if 'lunchout_Time2' in locals():
                if lunchout_Time2 and out_Time < lunchout_Time2:
                    raise forms.ValidationError("Your clock out time should be greater than saved lunch clock out")
            if 'lunchin_Time2' in locals():
                if lunchin_Time2  and out_Time < lunchin_Time2:
                    raise forms.ValidationError("Your out time should be greater than saved lunch clock in")
            if 'in_Time2' in locals() and 'lunchin_Time2' in locals() and 'lunchout_Time2' in locals():
                if (out_Time + (lunchout_Time2 + lunchin_Time2) - in_Time2).total_seconds() > 29700:
                    raise forms.ValidationError("cannot be clocked in for over eight hours")
            if 'lunchin_Time2' in locals() and 'lunchout_Time2' not in locals() and not lunchout_Time:
                raise forms.ValidationError("you cannot end your lunch break without starting one")
            if in_Time and lunchin_Time and not lunchout_Time:
                raise forms.ValidationError("you cannot end your lunch break without starting one")
        if lunchout_Time:
            if user is None:
                timecheck(lunchout_Time)
            if lunchin_Time and lunchout_Time < lunchin_Time:
                raise forms.ValidationError("Your lunch clock out time should be greater than lunch in out")
            if 'lunchin_Time2' not in locals() and lunchin_Time is None:
                raise forms.ValidationError("you cannout lunch clock out without lunch clocking in")
            if 'in_Time2' not in locals() and in_Time is None:
                raise forms.ValidationError("you cannot lunch clock out without clocking in")
            if 'lunchin_Time2' in locals(): 
                if lunchout_Time < lunchin_Time2:
                    raise forms.ValidationError("Your lunch clock out time should be greater than saved lunch in out")
                if (lunchout_Time - lunchin_Time2).total_seconds() > 2100:
                    raise forms.ValidationError("your lunch out time cannot be over 30 minutes")
            if in_Time and lunchout_Time < in_Time:
                raise forms.ValidationError("Your lunch clock out time should be greater than clock in")
            if 'in_Time2' in locals() and lunchout_Time < in_Time2:
                raise forms.ValidationError("your lunch clock out time should be greater than your saved clock in ")
        if lunchin_Time:
            if user is None:
                timecheck(lunchin_Time)
            if in_Time and lunchin_Time < in_Time:
                raise forms.ValidationError("Your lunch clock in time should be greater than clock in")
            if 'in_Time2' not in locals() and in_Time is None:
                raise forms.ValidationError("you cannot lunchin without clocking in")
            if 'in_Time2' in locals() and lunchin_Time < in_Time2:
                raise forms.ValidationError("your lunch clock in time should be greater than your saved clock in ")
        if in_Time:
            if user is None:
                timecheck(in_Time)
        if user is None:
            if not in_Time and not lunchin_Time and not lunchout_Time and not out_Time:
                raise forms.ValidationError("cannot have nothing filled in")
        return cleaned_data

# class timeEditFormSet(timeEditFormSet):
#     def full_clean(self):
#         cleaned_data = super.full_clean()
#         in_Time = cleaned_data.get("in_time")
#         lunchin_Time = cleaned_data.get("lunchin_time")
#         lunchout_Time = cleaned_data.get("lunchout_time")
#         out_Time = cleaned_data.get("out_time")
#         if out_Time:
#             timecheck(out_Time)
#             if lunchout_Time  and out_Time < lunchout_Time:
#                 raise forms.ValidationError("Your clock out time should be greater than lunch clock out")
#             if lunchin_Time  and out_Time < lunchin_Time:
#                 raise forms.ValidationError("Your lunch out time should be greater than lunch clock in")
#             if in_Time  and out_Time < in_Time:
#                 raise forms.ValidationError("Your clock out time should be greater than clock in")

def timecheck(date):
    if date.weekday() == 5 or date.weekday() == 6:
        raise forms.ValidationError("you cannot clock in on a weekend")
    time_right_now = timezone.now()
    dater = date - time_right_now
    if (dater).days < -1 or (dater).days > 0:
         raise forms.ValidationError("you can only clock in today")
    if date.hour < 5 or date.hour > 23:
        raise forms.ValidationError("you must clock in between 5 am and 11 pm")


        
#form for entering user for timeEdit
class UserForm(forms.ModelForm):
    class Meta: #used to create calander dropdown menus
        model = timeKeep
        fields = ["user",]

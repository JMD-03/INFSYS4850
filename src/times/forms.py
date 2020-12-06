from django import forms
from django.forms.widgets import DateTimeInput
from django.forms import ModelForm
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import datetime
from times.models import timeKeep

#input for widget
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

#form data
class timeForm(forms.ModelForm):
    class Meta: #used to create calander dropdown menus
        widgets = {'in_time': DateTimeInput(format='%Y-%m-%d %H:%M' ),
                   'lunchin_time': DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'lunchout_time': DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'out_time': DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'clocked_in': forms.HiddenInput(),
                   'is_Manual':forms.HiddenInput(),
                   'dateTimeEntered': forms.HiddenInput()
                   }
                   
        model = timeKeep
        fields = ["in_time", "lunchin_time", "lunchout_time", "out_time", "clocked_in", "dateTimeEntered"]

    
        #model function for manual time incase user goes out of bounds
    def clean(self):
        cleaned_data = super().clean()
        in_Time = cleaned_data.get("in_time")
        lunchin_Time = cleaned_data.get("lunchin_time")
        lunchout_Time = cleaned_data.get("lunchout_time")
        out_Time = cleaned_data.get("out_time")
        #datetimeEntered = cleaned_data.get("dateTimeEntered")
        #timeKeep.objects.filter(user = self.instance.user).get(dateTimeEntered = datetimeEntered.date())
        #print(timeKeep.in_time)
        if out_Time:
            timecheck(out_Time)
            if lunchout_Time  and out_Time < lunchout_Time:
                raise forms.ValidationError("Your clock out time should be greater than lunch clock out")
            if lunchin_Time  and out_Time < lunchin_Time:
                raise forms.ValidationError("Your lunch out time should be greater than lunch clock in")
            if in_Time  and out_Time < in_Time:
                raise forms.ValidationError("Your clock out time should be greater than clock in")
        if lunchout_Time:
            timecheck(lunchout_Time)
            if lunchin_Time and lunchout_Time < lunchin_Time:
                raise forms.ValidationError("Your lunch clock out time should be greater than lunch in out")
            if in_Time and lunchout_Time < in_Time:
                raise forms.ValidationError("Your lunch clock out time should be greater than clock in")
        if lunchin_Time:
            timecheck(lunchin_Time)
            if in_Time and lunchin_Time < in_Time:
                raise forms.ValidationError("Your lunch clock in time should be greater than clock in")
        if in_Time:
            timecheck(in_Time)
        if not in_Time and not lunchin_Time and not lunchout_Time and not out_Time:
            raise forms.ValidationError("cannot have nothing filled in")
        return cleaned_data
        
def timecheck(date):
    if date.weekday() == 5 or date.weekday() == 6:
        raise forms.ValidationError("you cannot clock in on a weekend")
    time_right_now = timezone.now()
    if (date - time_right_now).days > 7:
        raise forms.ValidationError("you must clock in within the week.")
    if (date - time_right_now).days < -1:
        raise forms.ValidationError("you cannot clock in before today")


        
#form for entering user for timeEdit
class UserForm(forms.ModelForm):
    class Meta: #used to create calander dropdown menus
        model = timeKeep
        fields = ["user",]
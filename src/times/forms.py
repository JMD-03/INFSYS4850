from django import forms
from django.forms.widgets import DateTimeInput
from django.forms import ModelForm
from django.contrib.auth.models import User
import datetime
from times.models import timeKeep

#input for widget
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

#form data
class timeForm(forms.ModelForm):
    class Meta: #used to create calander dropdown menus
        widgets = {'in_time': DateTimeInput(format='%Y-%m-%d %H:%M', ),
                   'lunchin_time': DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'lunchout_time': DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'out_time': DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'clocked_in': forms.HiddenInput(),
                   'currentDate': forms.HiddenInput(),
                   }
                   
        model = timeKeep
        fields = ["in_time", "lunchin_time", "lunchout_time", "out_time", "clocked_in", "currentDate"]


        #model function for manual time incase user goes out of bounds
    def clean(self):
        cleaned_data = super().clean()
        in_Time = cleaned_data.get("in_time")
        lunchin_Time = cleaned_data.get("lunchin_time")
        lunchout_Time = cleaned_data.get("lunchout_time")
        out_Time = cleaned_data.get("out_time")
        time_right_now = datetime.datetime.now().replace(tzinfo = None)
        if out_Time:
            if out_Time.weekday() == 5 or out_Time.weekday() == 6:
                raise forms.ValidationError("you cannot clock in on a weekend")
            if (out_Time.replace(tzinfo=None) - time_right_now).days > 7 or (out_Time.replace(tzinfo=None) - time_right_now).days < -1:
                raise forms.ValidationError("you must clock in within the week.(out)")
            if lunchout_Time  and out_Time < lunchout_Time:
                raise forms.ValidationError("Your clock out time should be greater than lunch clock out")
            if lunchin_Time  and out_Time < lunchin_Time:
                raise forms.ValidationError("Your lunch out time should be greater than lunch clock in")
            if in_Time  and out_Time < in_Time:
                raise forms.ValidationError("Your clock out time should be greater than clock in")
        if lunchout_Time:
            if lunchout_Time.weekday() == 5 or lunchout_Time.weekday() == 6:
                raise forms.ValidationError("you cannot clock in on a weekend")
            if (lunchout_Time.replace(tzinfo=None) - time_right_now).days > 7 or (lunchout_Time.replace(tzinfo=None) - time_right_now).days < -1:
                raise forms.ValidationError("you must clock in within the week.(lunchout)")
            if lunchin_Time and lunchout_Time < lunchin_Time:
                raise forms.ValidationError("Your lunch clock out time should be greater than lunch in out")
            if in_Time and lunchout_Time < in_Time:
                raise forms.ValidationError("Your lunch clock out time should be greater than clock in")
        if lunchin_Time:
            if lunchin_Time.weekday() == 5 or lunchin_Time.weekday() == 6:
                raise forms.ValidationError("you cannot clock in on a weekend")
            if (lunchin_Time.replace(tzinfo=None) - time_right_now).days > 7 or (lunchin_Time.replace(tzinfo=None) - time_right_now).days < -1:
                raise forms.ValidationError("you must clock in within the week(lunchin).")
            if in_Time and lunchin_Time < in_Time:
                raise forms.ValidationError("Your lunch clock in time should be greater than clock in")
        if in_Time:
            if in_Time.weekday() == 5 or in_Time.weekday() == 6:
                raise forms.ValidationError("you cannot clock in on a weekend")
            if (in_Time.replace(tzinfo=None) - time_right_now).days > 7 or (in_Time.replace(tzinfo=None) - time_right_now).days < -1:
                raise forms.ValidationError("you must clock in within the week.(in)")
        if not in_Time and not lunchin_Time and not lunchout_Time and not out_Time:
            raise forms.ValidationError("cannot have nothing filled in")
        return cleaned_data


        

class UserForm(forms.ModelForm):
    class Meta: #used to create calander dropdown menus
        model = timeKeep
        fields = ["user",]
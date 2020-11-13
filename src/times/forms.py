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
        widgets = {'in_time': DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'lunchin_time': DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'lunchout_time': DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'out_time': DateTimeInput(format='%Y-%m-%d %H:%M')}
        model = timeKeep
        fields = [ "in_time", "lunchin_time", "lunchout_time", "out_time", "clocked_in",]

        #model function for manual time incase user goes out of bounds
    def clean(self):
        cleaned_data = super().clean()
        in_Time = cleaned_data.get("in_time")
        lunchin_Time = cleaned_data.get("lunchin_time")
        lunchout_Time = cleaned_data.get("lunchout_time")
        out_Time = cleaned_data.get("out_time")
        if out_Time is not None:
            if out_Time < lunchout_Time:
                raise forms.ValidationError("Your clock out time should be greater than lunch clock out")
        if lunchout_Time is not None:
            if lunchout_Time < lunchin_Time:
                raise forms.ValidationError("Your lunch clock out time should be greater than lunch in out")
        if lunchin_Time is not None:
            if lunchin_Time < in_Time:
                raise forms.ValidationError("Your lunch clock in time should be greater than clock in")

   
from django import forms
from django.forms.widgets import DateTimeInput
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
        fields = ("PTO_Hours",
                  "Sick_Hours",
                  "PTO_Accrual_Rate",
                  "Sick_Accrual_Rate")


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class RequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RequestForm, self).__init__(*args, **kwargs)

    class Meta:
        widgets = {'start_Date_Time': DateTimeInput(format='%Y-%m-%d %H:%M'),
                   'end_Date_Time':   DateTimeInput(format='%Y-%m-%d %H:%M')}
        # widgets = {'start_Date': DateInput(),
        #            'end_Date':   DateInput(),
        #            'start_Time': TimeInput(format='%H:%M'),
        #            'end_Time': TimeInput(format='%H:%M')}
        model = Request
        # fields = ("request_Type", "start_Date",
        #           "end_Date", "start_Time", "end_Time")
        fields = ('request_Type','start_Date_Time','end_Date_Time')

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_Date_Time")
        end_date = cleaned_data.get("end_Date_Time")
        # start_time = cleaned_data.get("start_Time")
        # end_time = cleaned_data.get("end_Time")
        reqType = cleaned_data.get("request_Type")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")
        # if end_time < start_time:
        #     raise forms.ValidationError("End time should be greater than start time.")
        if reqType == "Paid Time Off Request":
            prof = self.user.id
            logging.warning(prof)
            pto = Profile.objects.get(user=prof)
            pto = pto.PTO_Hours
            logging.warning(pto)
            #calc_req = end_time - start_time
            #if pto_amount < calc_req:
            #    raise forms.ValidationError("You do not have enough PTO to cover this request.")



from django import forms
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


class RequestForm(forms.ModelForm):

    class Meta:
        widgets = {'start_Date': DateInput(),
                   'end_Date':   DateInput(),
                   'start_Time': TimeInput(format='%H:%M'),
                   'end_Time': TimeInput(format='%H:%M')}
        model = Request
        fields = ("request_Type", "start_Date",
                  "end_Date", "start_Time", "end_Time")

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_Date")
        end_date = cleaned_data.get("end_Date")
        start_time = cleaned_data.get("start_Time")
        end_time = cleaned_data.get("end_Time")
        reqType = cleaned_data.get("request_Type")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")
        if end_time < start_time:
            raise forms.ValidationError("End time should be greater than start time.")
        if reqType == "Paid Time Off Request":
            pto_amount = Profile.PTO_Hours
            # calc_req = end_time - start_time
            if pto_amount < calc_req:
                raise forms.ValidationError("You do not have enough PTO to cover this request.")



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
                   'start_Time': TimeInput(),
                   'end_Time': TimeInput()}
        model = Request
        fields = ("request_Type", "start_Date",
                  "end_Date", "start_Time", "end_Time")

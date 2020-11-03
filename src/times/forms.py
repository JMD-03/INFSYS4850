from django.utils import timezone
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
import datetime
from times.models import timeKeep

class timeForm(forms.ModelForm):
    in_time = forms.DateTimeField(initial = datetime.datetime.now(), disabled = True)

    class Meta:
        model = timeKeep
        readonly_fields = ["in_time"]
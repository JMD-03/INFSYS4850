from django import forms
from profiles.models import Profile
from times.models import timeKeep
from django.forms.widgets import DateTimeInput
from django.utils.timezone import datetime, timedelta, now


class ReportForm(forms.Form):
    times = (
        ("7", ("Last 7 Days")),
        ("14", ("Last 14 Days")),
        ("30", ("Last 30 Days")),
        ("90", ("Last 90 Days")),
        ("180", ("Last 180 Days")),
    )
    reports = (
        (1, ("Web-Based Report")),
        (2, ("Downloadable Report"))
    )
    time_Frame = forms.ChoiceField(choices=times, required=True)
    employee = [("all", "All Employees")]
    employee += [(i.user_id, i) for i in Profile.objects.all()]
    employee_Choice = forms.ChoiceField(choices=employee, required=True)
    report_Type = forms.ChoiceField(choices=reports, required=True)
    
    class Meta:
        fields: ('time_Frame', 'employee_Choice', 'report_Type')


class DateInput(forms.DateInput):
    input_type = 'date'

class ReportselfForm(forms.Form):
    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_Date")
        end_date = cleaned_data.get("end_Date")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

    reports = (
        (1, ("Web-Based Report")),
        (2, ("Downloadable Report"))
    )
    employee = [("all", "All Employees")]
    employee += [(i.user_id, i) for i in Profile.objects.all()]
    employee_Choice = forms.ChoiceField(choices=employee, required=True)
    report_Type = forms.ChoiceField(choices=reports, required=True)
    start_Date = forms.DateField(widget=DateInput)
    end_Date = forms.DateField(widget=DateInput)

    class Meta:
        fields: ('start_Date','end_Date', 'employee_Choice', 'report_Type')


class ReportTimePull(forms.Form):
    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("starting_Date")
        end_date = cleaned_data.get("ending_Date")
        print(end_date)
        print(start_date)
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

    reports = (
        (1, ("Web-Based Report")),
        (2, ("Downloadable Report"))
    )
    employee = [("all", "All Employees")]
    employee += [(i.user_id, i) for i in Profile.objects.all()]
    employee_Choice = forms.ChoiceField(choices=employee, required=True)
    report_Type = forms.ChoiceField(choices=reports, required=True)
    starting_Date = forms.DateField(widget=DateInput)
    ending_Date = forms.DateField(widget=DateInput)

    class Meta:
        fields: ('starting_Date','ending_Date', 'employee_Choice', 'report_Type')


#######################################

class ReportUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ReportUserForm, self).__init__(*args, **kwargs)
    times = (
        ("7", ("Last 7 Days")),
        ("14", ("Last 14 Days")),
        ("30", ("Last 30 Days")),
        ("90", ("Last 90 Days")),
        ("180", ("Last 180 Days")),
    )
    reports = (
        (1, ("Web-Based Report")),
        (2, ("Downloadable Report"))
    )
    time_Frame = forms.ChoiceField(choices=times, required=True)
    report_Type = forms.ChoiceField(choices=reports, required=True)
    
    class Meta:
        fields: ('time_Frame','report_Type')


class ReportselfUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ReportselfUserForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_Date")
        end_date = cleaned_data.get("end_Date")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

    reports = (
        (1, ("Web-Based Report")),
        (2, ("Downloadable Report"))
    )
    report_Type = forms.ChoiceField(choices=reports, required=True)
    start_Date = forms.DateField(widget=DateInput)
    end_Date = forms.DateField(widget=DateInput)

    class Meta:
        fields: ('start_Date','end_Date','report_Type')


class ReportTimeUserPull(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ReportTimeUserPull, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("starting_Date")
        end_date = cleaned_data.get("ending_Date")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

    reports = (
        (1, ("Web-Based Report")),
        (2, ("Downloadable Report"))
    )
    report_Type = forms.ChoiceField(choices=reports, required=True)
    starting_Date = forms.DateField(widget=DateInput)
    ending_Date = forms.DateField(widget=DateInput)

    class Meta:
        fields: ('starting_Date','ending_Date','report_Type')





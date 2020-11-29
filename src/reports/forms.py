from django import forms
from profiles.models import Profile
from times.models import timeKeep
from django.forms.widgets import DateTimeInput


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














    # def submit(self, *args, **kwargs):
    #     cleaned_data = super().clean()
    #     print(cleaned_data.get("employee_Choice"))
    #     print(cleaned_data.get("report_Type"))
    #     print(cleaned_data.get("time_Frame"))
    #     repType = cleaned_data.get("report_Type")
    #     tFrame = cleaned_data.get("time_Frame")

    #     profile = cleaned_data.get("employee_Choice")
    #     if profile == 'All':
    #         x = timeKeep.objects.all().order_by('user', 'in_time')
    #         print(timeKeep.objects.all())
    #         for obj in timeKeep.objects.all():
    #             print(obj.user)
    #         return x
    #     else:
    #         print("it didn't equal all")
    #     # prof = Profile.objects.get(user=prof)
    #     # pto = prof.PTO_Hours



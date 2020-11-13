from django import forms
from profiles.models import Profile


class ReportForm(forms.Form):
    times = (
        (1, ("Weekly")),
        (2, ("Bi-Weekly")),
        (3, ("Quarterly")),
        (4, ("Semi-Annually")),
    )
    reports = (
        (1, ("Web-Based Report")),
        (2, ("Downloadable Report"))
    )
    time_Frame = forms.ChoiceField(choices=times, required=True)
    employee = [("All", "All Employees")]
    employee += [(i, i) for i in Profile.objects.all()]
    employee_Choice = forms.ChoiceField(choices=employee, required=True)
    report_Type = forms.ChoiceField(choices=reports, required=True)


    class Meta:
        fields: ('time_Frame', 'employee_Choice', 'report_Type')

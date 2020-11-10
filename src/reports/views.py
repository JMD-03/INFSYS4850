from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required
@permission_required("reports.supervisor_view")
def reports_view(request, *args, **kwargs):
    return render(request, "reports.html", {})

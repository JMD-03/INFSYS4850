from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def reports_view(request, *args, **kwargs):
    return render(request, "reports.html", {})

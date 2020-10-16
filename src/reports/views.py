from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def reports_view(request, *args, **kwargs):
    return render(request, "reports.html", {})
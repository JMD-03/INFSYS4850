from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def signon_view(request, *args, **kwargs):
    return render(request, "signon.html", {})


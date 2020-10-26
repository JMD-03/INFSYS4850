from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import views
from times.views import timeEntry_view

# Create your views here.


def redirect_view(request, *args, **kwargs):
    print(request)
    if request.user.is_authenticated:
        return redirect('timeEntry')
    else:
        return redirect('login')

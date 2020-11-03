from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth

# Create your views here.


def redirect_login(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('timeEntry')
    else:
        return redirect('login')

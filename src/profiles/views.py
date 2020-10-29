from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm, ProfileForm, RequestForm

# Create your views here.


def profileCreation_view(request, *args, **kwargs):
    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = ProfileForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            form2 = form2.save(commit=False)
            form2.user = user
            form2.save()
            messages.success(request, 'New account was created successfully')
            return redirect('/admin')
    else:
        form1 = UserForm()
        form2 = ProfileForm()
        #messages.warning(request, 'Account Creation Failed')
    return render(request, 'profileCreation.html', {'form1': form1, 'form2': form2})


def requests_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin')
    else:
        form = RequestForm()
    return render(request, 'requests.html', {'form': form})

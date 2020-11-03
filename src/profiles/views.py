from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm, ProfileForm, RequestForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
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

@login_required
def requests_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            form.save()
            #Need to fix the redirect, this is just for testing
            return redirect('/admin')
    else:
        form = RequestForm()
    return render(request, 'requests.html', {'form': form})

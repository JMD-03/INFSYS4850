from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserCreateForm

# Create your views here.

def profileCreation_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
           # messages.success(request, 'Account Created Successfully')
            return redirect('profileCreation')
    else:
        form = UserCreateForm()
        #messages.warning(request, 'Account Creation Failed')
    return render(request, 'profileCreation.html', {'form': form})
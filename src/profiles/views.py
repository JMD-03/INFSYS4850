from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm, ProfileForm

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
            messages.success(request, 'Account Created Successfully')
            return redirect('profileCreation')
    else:
        form1 = UserForm(request.POST)
        form2 = ProfileForm(request.POST)
        messages.warning(request, 'Account Creation Failed')
    return render(request, 'profileCreation.html', {'form1': form1, 'form2': form2})

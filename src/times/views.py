from times.forms import timeForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime

# core logic

@login_required
def timeEntry_view(request, *args, **kwargs):	
	if request.method == 'POST':
		form = timeForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'time saved!')
			return redirect('timeEntry.html')
	else:
		form = timeForm()
		messages.warning(request, "could not save time")


	return render(request, 'timeEntry.html', {'form' : form})
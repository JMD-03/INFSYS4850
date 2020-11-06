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
			return redirect('/admin')
	else:
		form = timeForm()

	return render(request, 'timeEntry.html', {'form' : form})
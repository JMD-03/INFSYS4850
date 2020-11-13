from times.forms import timeForm
from times.models import timeKeep
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime

# core logic

@login_required
def timeEntry_view(request, *args, **kwargs):	
	if request.method == 'POST':
		form = timeForm(request.POST)
		if form.is_valid():
			user = form.save()
			if 'autoIn' in request.POST:
				date = datetime.now()
				user.in_time = date.strftime('%Y-%m-%d %H:%M')
				user.clocked_in = True
			if 'autoOut' in request.POST:
				date = datetime.now()
				user.out_time = date.strftime('%Y-%m-%d %H:%M')
				user.clocked_out = False
			user.user = request.user
			user.save()
			return redirect('/admin')
	else:
		form = timeForm()
	return render(request, 'timeEntry.html', {'form' : form})
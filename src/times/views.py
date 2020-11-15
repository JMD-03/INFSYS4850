from times.forms import timeForm
from times.models import timeKeep
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime

# core logic

@login_required
def timeEntry_view(request, *args, **kwargs):	
	try:
		current = timeKeep.objects.filter(user = request.user).get(currentDate = datetime.date.today())
	except timeKeep.DoesNotExist:
		current = timeKeep.objects.create(user = request.user, currentDate = datetime.date.today())
	if request.method == 'POST':
		if 'autoIn' in request.POST:
			date = datetime.datetime.now()
			current.in_time = date
			current.clocked_in = True
			#print("autoin")
		if 'lunchIn' in request.POST:
			date = datetime.datetime.now()
			current.lunchin_time = date
			current.clocked_in = False
		if 'lunchOut' in request.POST:
			date = datetime.datetime.now()
			current.lunchout_time = date
			current.clocked_in = True
		if 'autoOut' in request.POST:
			date = datetime.datetime.now()
			current.out_time = date
			current.clocked_in = False
			#print("autoout")
		current.save()
		return redirect('/admin')
	else:
		form = timeForm(instance = current)
	return render(request, 'timeEntry.html', {'form' : form})
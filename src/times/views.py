from times.models import timeKeep

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

import datetime

# core logic


def timeEntry_view(request):	
	try:
		current_cs = timeKeep.objects.get(user = request.user, clocked_in = True)
	except timeKeep.DoesNotExist:
		current_cs = None
	except timeKeep.MultipleObjectsReturned:
		return HttpResponse('An error has occurred. Multiple unclosed clock-ins are recorded. ' + 
							'Please ask an admin to manually clock you out of a previous session.')

	#finding monday
	today = datetime.date.today()
	last_monday = today - datetime.timedelta(days = today.weekday())
	recent_sessions = timeKeep.objects.filter(user = request.user, in_time__gte = last_monday)
	
	return render(request, 'timeEntry.html', {'cs': current_cs, 'user': request.user, 'rs': recent_sessions})

def clock_in(request):
	try:
		cs = timeKeep.objects.get(user = request.user, clocked_in = True)
		return HttpResponseRedirect(reverse('timeKeep:time'))
	except timeKeep.DoesNotExist:
		cs = timeKeep(user = request.user)
		cs.clock_in()
		return HttpResponseRedirect(reverse('timeKeep:time'))

def clock_out(request):
	try:
		cs = timeKeep.objects.get(user = request.user, clocked_in = True)
		cs.clock_out()
		return HttpResponseRedirect(reverse('timeKeep:time'))
	except timeKeep.DoesNotExist:
		return HttpResponseRedirect(reverse('timeKeep:time'))
	except timeKeep.MultipleObjectsReturned:
		return HttpResponse('Error: You are clocked in multiple times. Please have an admin correct this manually.')

def	lunch_in(request):
		try: 
			cs = timeKeep.objects.get(user = request.user, clocked_in = True)
			cs.lunch_in()
			return HttpResponseRedirect(reverse('timeKeep:time'))
		except timeKeep.DoesNotExist:
			return HttpResponseRedirect(reverse('timeKeep:time'))

def lunch_out(request):
		try:
			cs = timeKeep.objects.get(user = request.user, clocked_in = True)
			cs.lunch_out()
			return HttpResponseRedirect(reverse('timeKeep:time'))
		except timeKeep.DoesNotExist:
			return HttpResponseRedirect(reverse('timeKeep:time'))
		except timeKeep.MultipleObjectsReturned:
			return HttpResponse('Error too many clock ins')

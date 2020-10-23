from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from times.models import timekeep
import datetime
# Create your views here.
def timeEntry_view(request):
    #checking to see if the user is actually clocked in
    try:
        current_tk = timekeep.objects.get(user = request.user, clocked = True)
    except timekeep.DoesNotExist:
        current_tk = None
    except timekeep.MultipleObjectsReturned:
        return HttpResponse('an error has occured as multiple clock ins are being recorded')

    #finding monday/first day of the week
    today = datetime.date.today()
    last_monday = today - datetime.timedelta(days = today.weekday())
    recent_time = timekeep.objects.filter(user = request.user, in_time_gte = last_monday)
    
    return render(request, "timeEntry.html", {'tk': current_tk, 'user':request.user, 'rs': recent_sessions})

def clock_in(request):
    try: 
        tk = timekeep.objects.get(user = request.user, clocked = True)
        return HttpResponseRedirect(reverse('times:timekeep'))
    except timekeep.DoesNotExist:
        tk = timekeep(user = request.user)
        tk.clocked_in()
        return HttpResponseRedirect(reverse('times:timekeep'))
def clock_out(request):
    try:
        tk = timekeep.objects.get(user = request.user, clocked = True)
        tk.clocked_out()
        return HttpResponseRedirect(reverse('times:timekeep'))
    except timekeep.DoesNotExist:
        return HttpResponseRedirect(reverse('times:timekeep'))
    except timekeep.MultipleObjectsReturned:
        return HttpResponse('Error: you have clocked in multiple times')
from times.forms import timeForm, UserForm
from django.forms import HiddenInput, TimeInput, DateTimeInput
from times.models import timeKeep
from django.forms import modelformset_factory, model_to_dict
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.forms.widgets import TextInput
from django.db import connection
from django.utils import timezone
from django.utils.timezone import datetime
from django.http import HttpResponseServerError


# core logic

timeEditFormSet = modelformset_factory(timeKeep, extra = 5, max_num = 5, fields=("in_time", "lunchin_time", "lunchout_time", "out_time", "dateTimeEntered", "user", "week_number"), widgets={"dateTimeEntered": HiddenInput(), "user": HiddenInput(), "week_number":HiddenInput()})
formsetInitParams = []

@login_required
def timeEntry_view(request, *args, **kwargs):	
	current = getTimeKeepFromKeys(request.user,'Standard Time', timezone.now())
	if current == "MultiObj":
		return HttpResponseServerError("Can't have more than one time entry per day, Please Contact Management/Supervisors. /n Hit the back button to go back")
	if request.method == 'POST':
		currentReqForm = timeForm(request.POST)
		if currentReqForm.is_valid():
			#currentReqForm.save()
			if 'manual' in request.POST and currentReqForm.is_valid():
				if 'in_time' in currentReqForm.changed_data:
					in_time = currentReqForm.cleaned_data['in_time']
					inCurrent = getTimeKeepFromKeys(request.user,'Standard Time', in_time, True)
					inCurrent.in_time = in_time
					inCurrent.dateTimeEntered = in_time.date()
					inCurrent.week_number = in_time.isocalendar().week
					inCurrent.clocked_in = True
					inCurrent.is_Manual = True
					inCurrent.save()
				if 'lunchin_time' in currentReqForm.changed_data:
					lunchin_time = currentReqForm.cleaned_data['lunchin_time']
					inCurrent = getTimeKeepFromKeys(request.user,'Standard Time', lunchin_time, True)
					inCurrent.lunchin_time = lunchin_time
					inCurrent.dateTimeEntered = lunchin_time.date()
					inCurrent.week_number = lunchin_time.isocalendar().week
					inCurrent.clocked_in = False
					inCurrent.is_Manual = True
					inCurrent.save()
				if 'lunchout_time' in currentReqForm.changed_data:
					lunchout_time = currentReqForm.cleaned_data['lunchout_time']
					inCurrent = getTimeKeepFromKeys(request.user, 'Standard Time',lunchout_time, True)
					inCurrent.lunchout_time = lunchout_time
					inCurrent.dateTimeEntered = lunchout_time.date()
					inCurrent.week_number = lunchout_time.isocalendar().week
					inCurrent.clocked_in = True
					inCurrent.is_Manual = True
					inCurrent.save()
				if 'out_time' in currentReqForm.changed_data:
					out_time = currentReqForm.cleaned_data['out_time']
					inCurrent = getTimeKeepFromKeys(request.user,'Standard Time', out_time, True)
					inCurrent.out_time = out_time
					inCurrent.dateTimeEntered = out_time.date()
					inCurrent.week_number = out_time.isocalendar().week
					inCurrent.clocked_in = False
					inCurrent.is_Manual = True
					inCurrent.save()
		else:
			# Error area
			current = getTimeKeepFromKeys(request.user,'Standard Time', timezone.now(), True)
			date = timezone.now()
			if 'autoIn' in request.POST:
				current.in_time = date
				current.clocked_in = True
				#print("autoin")
				current.save()
			elif 'lunchIn' in request.POST:
				current.lunchin_time = date
				current.clocked_in = False
				current.save()
			elif 'lunchOut' in request.POST:
				current.lunchout_time = date
				current.clocked_in = True
				current.save()
			elif 'autoOut' in request.POST:
				current.out_time = date
				current.clocked_in = False
				current.save()
				#print("autoout")
			else:
				return render(request, 'timeEntry.html', {'form' : currentReqForm})
		return redirect('/admin/times/timekeep')
	else:
		if not current:
			current = timeKeep(user = request.user,dateTimeEntered = timezone.now())
		form = timeForm(instance = current)
	return render(request, 'timeEntry.html', {'form' : form})

def getTimeKeepFromKeys(user, timeType, date, create = False):
	try:
		return timeKeep.objects.filter(user = user, timeType = timeType).get(dateTimeEntered = date.date())
	except timeKeep.DoesNotExist:
		if create:
			return timeKeep.objects.create(user = user, timeType = timeType, dateTimeEntered = date.date())
	except timeKeep.MultipleObjectsReturned:
		return "MultiObj"
	return None

@login_required
@permission_required("reports.supervisor_view", "reports.management_view")
def timeEdit_view(request, *args, **kwargs):
	global formsetInitParams
	if 'user' not in request.POST:
		if 'weeklyTimeSubmit' in request.POST:
			currentDayForms = timeEditFormSet(request.POST, initial = formsetInitParams, queryset = timeKeep.objects.none())
			for form in currentDayForms:
				if form.has_changed() and form.is_valid():
					user = form.cleaned_data['user']
					dateTimeEntered = form.cleaned_data['dateTimeEntered']
					currentFormTimeKeep = getTimeKeepFromKeys(user, 'Standard Time', dateTimeEntered, True)
					currentFormTimeKeep.in_time = form.cleaned_data['in_time']
					currentFormTimeKeep.lunchin_time = form.cleaned_data['lunchin_time']
					currentFormTimeKeep.lunchout_time = form.cleaned_data['lunchout_time']
					currentFormTimeKeep.out_time = form.cleaned_data['out_time']
					currentFormTimeKeep.save()
			return render(request, 'timeEdit.html', {'userformset': currentDayForms})
		else:
			userform = UserForm()
			return render(request, 'timeEdit.html', {'form': userform, 'onlyuser': True})
			
	else:
		userform = UserForm(request.POST)
		if not userform.is_valid():
			return render(request, 'timeEdit.html', {'form': UserForm(), 'onlyuser': True})
		user = userform.cleaned_data['user']
		year = timezone.now().isocalendar().year
		weekNumberToday = timezone.now().isocalendar().week
		datesToDisplay = [datetime.strptime(f'{year}-W{weekNumberToday - 1}-{i}', "%Y-W%W-%w") for i in range (1,6)]
		formsetInitParams = []
		for date in datesToDisplay:
			param = None
			if getTimeKeepFromKeys(user,'Standard Time', date, False) == None:
				param = {'user': user, 'dateTimeEntered': date.date()}
			else:
				param =  model_to_dict(getTimeKeepFromKeys(user,'Standard Time', date, False))
			formsetInitParams.append(param)
		currentDayForms = timeEditFormSet(initial=formsetInitParams, queryset = timeKeep.objects.none())
		return render(request, 'timeEdit.html', {'userformset': currentDayForms})
	#def my_custom_sql(self):
		#with connection.cursor() as cursor:
			#cursor.execute("SELECT in_time FROM times_timekeep WHERE in_time BETWEEN 2020-11-24 AND 2020-11-31")
			#cursor.fetchall()

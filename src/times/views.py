from times.forms import timeForm, UserForm
from django.forms import HiddenInput, TimeInput, DateTimeInput
from times.models import timeKeep
from django.forms import modelformset_factory, model_to_dict
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.forms.widgets import TextInput
import datetime

# core logic

timeEditFormSet = modelformset_factory(timeKeep, extra = 5, max_num = 5, fields=("in_time", "lunchin_time", "lunchout_time", "out_time", "dateTimeEntered", "user"), widgets={"dateTimeEntered": HiddenInput(), "user": HiddenInput()})
formsetInitParams = []

@login_required
def timeEntry_view(request, *args, **kwargs):	
	current = getTimeKeepFromKeys(request.user, timezone.localtime(timezone.now()))
	if request.method == 'POST':
		currentReqForm = timeForm(request.POST)
		if currentReqForm.is_valid():
			#currentReqForm.save()
			if 'manual' in request.POST and currentReqForm.is_valid():
				if 'in_time' in currentReqForm.changed_data:
					in_time = currentReqForm.cleaned_data['in_time']
					inCurrent = getTimeKeepFromKeys(request.user, in_time, True)
					inCurrent.in_time = in_time
					inCurrent.dateTimeEntered = in_time
					inCurrent.clocked_in = True
					inCurrent.save()
				if 'lunchin_time' in currentReqForm.changed_data:
					lunchin_time = currentReqForm.cleaned_data['lunchin_time']
					inCurrent = getTimeKeepFromKeys(request.user, lunchin_time, True)
					inCurrent.lunchin_time = lunchin_time
					inCurrent.dateTimeEntered = lunchin_time
					inCurrent.clocked_in = False
					inCurrent.save()
				if 'lunchout_time' in currentReqForm.changed_data:
					lunchout_time = currentReqForm.cleaned_data['lunchout_time']
					inCurrent = getTimeKeepFromKeys(request.user, lunchout_time, True)
					inCurrent.lunchout_time = lunchout_time
					inCurrent.dateTimeEntered = lunchout_time
					inCurrent.clocked_in = True
					inCurrent.save()
				if 'out_time' in currentReqForm.changed_data:
					out_time = currentReqForm.cleaned_data['out_time']
					inCurrent = getTimeKeepFromKeys(request.user, out_time, True)
					inCurrent.out_time = out_time
					inCurrent.dateTimeEntered = out_time
					inCurrent.clocked_in = False
					inCurrent.save()
		else:
			# Error area
			current = getTimeKeepFromKeys(request.user, timezone.now(), True)
			date = timezone.localtime(timezone.now())
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
		if current:
			form = timeForm(instance = current)
		else:
			form = timeForm()
	return render(request, 'timeEntry.html', {'form' : form})

def getTimeKeepFromKeys(user, date, create = False):
	try:
		return timeKeep.objects.filter(user = user).get(dateTimeEntered = date)
	except timeKeep.DoesNotExist:
		if create:
			return timeKeep.objects.create(user = user, dateTimeEntered = date)
		else:
			return None
	return None

@login_required
@permission_required("reports.supervisor_view", "reports.management_view")
def timeEdit_view(request, *args, **kwargs):
	global formsetInitParams
	if 'user' not in request.POST:
		if 'weeklyTimeSubmit' in request.POST:
			currentDayForms = timeEditFormSet(request.POST, initial = formsetInitParams)
			#for form in currentDayForms:
				#if form.has_changed():
					#timeKeep = form.save(commit = False)
					#dateTimeEntered = form.cleaned_data_['dateTimeEntered']
					#timeKeep.in_time += dateTimeEntered
			if currentDayForms.has_changed() and currentDayForms.is_valid():
				currentDayForms.save()
			return render(request, 'timeEdit.html', {'userformset': currentDayForms})
		else:
			userform = UserForm()
			return render(request, 'timeEdit.html', {'form': userform, 'onlyuser': True})

	else:
		userform = UserForm(request.POST)
		if not userform.is_valid():
			return render(request, 'timeEdit.html', {'form': UserForm(), 'onlyuser': True})
		user = userform.cleaned_data['user']
		year = datetime.datetime.now().isocalendar().year
		weekNumberToday = datetime.datetime.now().isocalendar().week
		datesToDisplay = [datetime.datetime.strptime(f'{year}-W{weekNumberToday - 1}-{i}', "%Y-W%W-%w") for i in range (1,6)]
		formsetInitParams = []
		for date in datesToDisplay:
			param = None
			if getTimeKeepFromKeys(user, date, False) == None:
				param = {'user': user, 'dateTimeEntered': date.date()}
			else:
				param =  model_to_dict(getTimeKeepFromKeys(user, date, False))
			formsetInitParams.append(param)
		currentDayForms = timeEditFormSet(initial=formsetInitParams, queryset = timeKeep.objects.none())
		return render(request, 'timeEdit.html', {'userformset': currentDayForms})

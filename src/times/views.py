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
	return render(request, 'timeEdit.html')
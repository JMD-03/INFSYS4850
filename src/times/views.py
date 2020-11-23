from times.forms import timeForm, UserForm, DateTimeInput
from django.forms import HiddenInput
from times.models import timeKeep
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.forms.widgets import TextInput

# core logic

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
					inCurrent.currentDate = in_time
					inCurrent.clocked_in = True
					inCurrent.save()
				if 'lunchin_time' in currentReqForm.changed_data:
					lunchin_time = currentReqForm.cleaned_data['lunchin_time']
					inCurrent = getTimeKeepFromKeys(request.user, lunchin_time, True)
					inCurrent.lunchin_time = lunchin_time
					inCurrent.currentDate = lunchin_time
					inCurrent.clocked_in = False
					inCurrent.save()
				if 'lunchout_time' in currentReqForm.changed_data:
					lunchout_time = currentReqForm.cleaned_data['lunchout_time']
					inCurrent = getTimeKeepFromKeys(request.user, lunchout_time, True)
					inCurrent.lunchout_time = lunchout_time
					inCurrent.currentDate = lunchout_time
					inCurrent.clocked_in = True
					inCurrent.save()
				if 'out_time' in currentReqForm.changed_data:
					out_time = currentReqForm.cleaned_data['out_time']
					inCurrent = getTimeKeepFromKeys(request.user, out_time, True)
					inCurrent.out_time = out_time
					inCurrent.currentDate = out_time
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
		return timeKeep.objects.filter(user = user).get(currentDate = date)
	except timeKeep.DoesNotExist:
		if create:
			return timeKeep.objects.create(user = user, currentDate = date)
	return None

@login_required
@permission_required("reports.supervisor_view", "reports.management_view")
def timeEdit_view(request, *args, **kwargs):
	if 'user' not in request.POST:
		userform = UserForm()
		return render(request, 'timeEdit.html', {'form': userform, 'onlyuser': True})
	else:
		userform = UserForm(request.POST)
		if not userform.is_valid():
			return render(request, 'timeEdit.html', {'form': UserForm(), 'onlyuser': True})
		timeEditFormSet = modelformset_factory(timeKeep, extra = 0, fields=("in_time", "lunchin_time", "lunchout_time", "out_time", "currentDate",), widgets={"currentDate": HiddenInput()})
		currentDayForms = timeEditFormSet(queryset = timeKeep.objects.filter(user__exact=userform.cleaned_data['user']))
		for form in currentDayForms:
			form.fields["currentDate"].disabled = True
		return render(request, 'timeEdit.html', {'userformset': currentDayForms})
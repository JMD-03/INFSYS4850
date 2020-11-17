from times.forms import timeForm
from times.models import timeKeep
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from django.utils import timezone

# core logic

@login_required
def timeEntry_view(request, *args, **kwargs):	
	current = getTimeKeepFromKeys(request.user, timezone.localtime(timezone.now()))
	if request.method == 'POST':
		currentReqForm = timeForm(request.POST)
		if currentReqForm.is_valid():
			if 'manual' in request.POST:
				print(currentReqForm)
				if 'in_time' in currentReqForm.changed_data:
					in_time = currentReqForm.cleaned_data['in_time']
					inCurrent = getTimeKeepFromKeys(request.user, in_time, True)
					inCurrent.in_time = in_time
					inCurrent.currentDate = in_time
					inCurrent.save()
				if 'lunchin_time' in currentReqForm.changed_data:
					lunchin_time = currentReqForm.cleaned_data['lunchin_time']
					inCurrent = getTimeKeepFromKeys(request.user, lunchin_time, True)
					inCurrent.lunchin_time = lunchin_time
					inCurrent.currentDate = lunchin_time
					inCurrent.save()
				if 'lunchout_time' in currentReqForm.changed_data:
					lunchout_time = currentReqForm.cleaned_data['lunchout_time']
					inCurrent = getTimeKeepFromKeys(request.user, lunchout_time, True)
					inCurrent.lunchout_time = lunchout_time
					inCurrent.currentDate = lunchout_time
					inCurrent.save()
				if 'out_time' in currentReqForm.changed_data:
					out_time = currentReqForm.cleaned_data['out_time']
					inCurrent = getTimeKeepFromKeys(request.user, out_time, True)
					inCurrent.out_time = out_time
					inCurrent.currentDate = out_time
					inCurrent.save()
			else:
				current = getTimeKeepFromKeys(request.user, timezone.now(), True)
				date = timezone.localtime(timezone.now())
				if 'autoIn' in request.POST:
					current.in_time = date
					current.clocked_in = True
					#print("autoin")
				elif 'lunchIn' in request.POST:
					current.lunchin_time = date
					current.clocked_in = False
				elif 'lunchOut' in request.POST:
					current.lunchout_time = date
					current.clocked_in = True
				elif 'autoOut' in request.POST:
					current.out_time = date
					current.clocked_in = False
					#print("autoout")
				current.save()
		return redirect('/admin')
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
	return render(request, 'timeEdit.html')
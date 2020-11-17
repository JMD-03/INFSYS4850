from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ReportForm

# Create your views here.
@login_required
@permission_required("pages.supervisor_view")
def reports_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            #form.save()
            #Rather than form.save() I need to call a procedure with those parameters passed
            return redirect('/admin')
    else:
        form = ReportForm()
    return render(request, 'reports.html', {'form': form})

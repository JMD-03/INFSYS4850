from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ReportForm
from django.db import connections, connection
from times.models import timeKeep
from django.utils.timezone import datetime, timedelta, now
from django.utils import timezone, dateformat
import csv
from django.template import loader

# Create your views here.
@login_required
@permission_required("pages.supervisor_view")
def reports_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['time_Frame'])
            time = form.cleaned_data['time_Frame']
            #print(form.cleaned_data['employee_Choice'])
            user_id = form.cleaned_data['employee_Choice']
            if user_id == "all":
                user_id = '%'
            print(user_id)

            
            ### This needs to be parameterized and pull proper data based on the employee and time frame passed. Right now it gets all data for all time
            ### Also have to take out lunch times from the total time worked
            def my_custom_sql():
                with connection.cursor() as cursor:
                    row = ("Time Report Run At ", datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'),".","\n")
                    row += ("This report was run for the previous ", time, " days." "\n")
                    row += ("Employee Name, ", "Time Type, ", "Total Hours Logged, ","Number of Time Entries ", "\n")
                    cursor.execute("select concat(au.first_name, ' ', au.last_name), tt.timeType, CASE WHEN tt.lunchin_time IS NULL AND tt.lunchout_time IS NULL THEN sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2)) ELSE sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, tt.lunchin_time, tt.lunchout_time)/60),2))END, count(timeType) FROM times_timekeep tt JOIN auth_user au ON au.id = tt.user_id WHERE curdate() - %s <= tt.in_time AND tt.user_id LIKE %s GROUP BY 1, 2", [time, user_id])
                    for rows in cursor.fetchall():
                        row += (rows[0], ", ",rows[1],", ",rows[2],", ",rows[3],", ", "\n")
                    row += ("\n",)
                    row += ("The decimal is a percentage of an hour (ex .5 = 30minutes)",)
                return row
            if form.cleaned_data['report_Type'] == '1':          #### This is for web view. The else is for downloading file
                ##Ugly but working code, comments below are testing code that failed.
                response = HttpResponse(my_custom_sql(), "")
                response['Content-Disposition'] = 'inline; filename="report.csv"'
            else:
                response = HttpResponse(my_custom_sql(), content_type='application/text charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="report.csv"'
            return response
    else:
        form = ReportForm()
    return render(request, 'reports.html', {'form': form})

def reports_webview(request, *args, **kwargs):
    pass
        

#spare code I didn't want to delete yet around downloading files


            # def dictfetchall(cursor):
            #     #"Return all rows from a cursor as a dict"
            #     columns = [col[0] for col in cursor.description]
            #     print(columns)
            #     print()
            #     return [
            #         dict(zip(columns, row))
            #         for row in cursor.fetchall()]

            #cursor.callproc('gather_report', [1,"All",1,0])
            #print(cursor.fetchall())
            #result_set = cursor.fetchall()

##Example SQL query to database
    # cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
    # cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])


    ##Attempted to fix formatting, but this doesn't work on dates
    # [', '.join(map(str, x)) for x in rows.first_name]


    # response = HttpResponse(my_custom_sql(), "pdf") #mimetype='application.pdf')
    # response['Content-Disposition'] = 'inline; filename="report.pdf"'

    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = 'inline; filename="report.csv"'
    # writer = csv.writer(response)
    # writer.writerow(my_custom_sql())

    #response = HttpResponse(my_custom_sql(), 'reports_webview.html')
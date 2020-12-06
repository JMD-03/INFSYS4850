from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ReportForm,ReportselfForm, ReportTimePull, ReportUserForm, ReportselfUserForm, ReportTimeUserPull
from django.db import connection
from django.utils.timezone import datetime, timedelta, now
from django.utils import timezone, dateformat
from times.models import timeKeep
import re


@login_required
def reports_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        form2 = ReportselfForm(request.POST)
        form3 = ReportTimePull(request.POST)

        if form.is_valid() and 'predefined' in request.POST:
            time = form.cleaned_data['time_Frame']
            user_id = form.cleaned_data['employee_Choice']
            if user_id == "all":
                user_id = '%'

            def my_custom_sql():
                with connection.cursor() as cursor:
                    try:
                        row = ("Time Report Run At ", datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'),".","\n")
                        row += ("This report was run for the previous ", time, " days." "\n")
                        if form.cleaned_data['report_Type'] == '1':
                            row += ("Employee Name","\t", " Time Type ", "\t", "Total Hours Logged, ","\t"," Number of Time Entries ", "\n")
                        else:
                            row += ("Employee Name, ", " Time Type, ", " Total Hours Logged, "," Number of Time Entries ", "\n")
                        cursor.execute("select concat(au.first_name, ' ', au.last_name), tt.timeType, CASE when tt.lunchin_time IS NULL AND tt.lunchout_time IS NULL THEN sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2)) WHEN tt.lunchin_time IS NULL and tt.lunchout_time IS NOT NULL THEN sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, DATE_SUB(tt.lunchout_time, INTERVAL 30 MINUTE), tt.lunchout_time)/60),2)) WHEN tt.lunchin_time IS NOT NULL and tt.lunchout_time IS NULL THEN sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, tt.lunchin_time, DATE_ADD(tt.lunchin_time, INTERVAL 30 MINUTE))/60),2)) ELSE sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, tt.lunchin_time, tt.lunchout_time)/60),2)) END, count(timeType) FROM times_timekeep tt JOIN auth_user au ON au.id = tt.user_id WHERE tt.in_time BETWEEN DATE_ADD(DATE_SUB(curdate(), INTERVAL %s DAY), INTERVAL 6 HOUR) AND date_add(curdate(), INTERVAL 30 HOUR) AND tt.user_id LIKE %s GROUP BY 1, 2", [time, user_id])
                        if form.cleaned_data['report_Type'] == '1':
                            for rows in cursor.fetchall():
                                row += (rows[0], "\t ", rows[1], "\t ", rows[2], "\t ", rows[3], "\n")
                        else:
                            for rows in cursor.fetchall():
                                row += (rows[0],",", rows[1],",", rows[2],",", rows[3], "\n")
                        row += ("\n",)
                        row += ("The decimal is a percentage of an hour (ex .5 = 30minutes)",)
                    except:
                        row += ("There was an error processing the report request. Please try again.",)
                    finally:
                        cursor.close()
                return row

            if form.cleaned_data['report_Type'] == '1':          #### This is for web view. The else is for downloading file
                response = HttpResponse(my_custom_sql(), "")
                response['Content-Disposition'] = 'inline; filename="report.csv"'
            else:
                response = HttpResponse(my_custom_sql(), content_type='application/text charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="report.csv"'
            return response

        elif form3.is_valid() and 'timeEntry' in request.POST:
            start = form3.cleaned_data['starting_Date']
            end = form3.cleaned_data['ending_Date']
            user_id = form3.cleaned_data['employee_Choice']
            if user_id == "all":
                user_id = '%'
            dF = '%Y-%m-%d %H:%i'

            def my_custom_sql():
                with connection.cursor() as cursor:
                    try:
                        row = ("Time Report Run At ", datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'),".","\n")
                        row += ("This report was run for the following dates: ", start, " through ", end, "." "\n")
                        if form3.cleaned_data['report_Type'] == '1':
                            row += ("Employee Name    ", "Clocked In       ", "  Lunch Start "," Lunch End   ","Clocked Out ","\t", " Time Type      ", "Manual Entry", "\n")
                        else:
                            row += ("Employee Name, ", " Clocked In , ", " Lunch Start, "," Lunch End, "," Clocked Out , ", " Time Type, ", "Manual Entry", "\n")
                        cursor.execute("select concat(au.first_name, ' ', au.last_name), DATE_FORMAT(DATE_SUB(in_time, INTERVAL 6 HOUR), %s),DATE_FORMAT(DATE_SUB(lunchin_time, INTERVAL 6 HOUR), %s), DATE_FORMAT(DATE_SUB(lunchout_time, INTERVAL 6 HOUR), %s), DATE_FORMAT(DATE_SUB(out_time, INTERVAL 6 HOUR), %s), timeType, is_Manual FROM times_timekeep tt JOIN auth_user au ON au.id = tt.user_id WHERE tt.in_time BETWEEN DATE_ADD(%s, INTERVAL 6 HOUR) AND DATE_ADD(%s, INTERVAL 30 HOUR) AND tt.user_id LIKE %s ORDER BY 2,1", [dF, dF, dF, dF, start, end, user_id])
                        if form3.cleaned_data['report_Type'] == '1':
                            for rows in cursor.fetchall():
                                if rows[6] == 0:
                                    row += (rows[0], "\t ",rows[1],"\t ",rows[2],"\t ",rows[3],"\t ", rows[4], "\t ",rows[5],"\t ","False", "\n")
                                else:
                                    row += (rows[0], "\t ",rows[1],"\t ",rows[2],"\t ",rows[3],"\t ", rows[4], "\t ",rows[5],"\t ","True", "\n")
                        else:
                            for rows in cursor.fetchall():
                                if rows[6] == 0:
                                    row += (rows[0], ",",rows[1],",",rows[2],",",rows[3],",", rows[4], ",",rows[5],",","False", "\n")
                                else:
                                    row += (rows[0], ",",rows[1],", ",rows[2],",",rows[3],",", rows[4], ", ",rows[5],",","True", "\n")
                        row += ("\n",)
                        row += ("The decimal is a percentage of an hour (ex .5 = 30minutes)",)
                    except:
                        row += ("There was an error while processing the request",)
                    finally:
                        cursor.close()
                return row

            if form3.cleaned_data['report_Type'] == '1':          #### This is for web view. The else is for downloading file
                response = HttpResponse(my_custom_sql(), "")
                response['Content-Disposition'] = 'inline; filename="report.csv"'
            else:
                response = HttpResponse(my_custom_sql(), content_type='application/text charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="report.csv"'
            return response

        elif form2.is_valid() and 'customSummary' in request.POST:
            start = form2.cleaned_data['start_Date']
            end = form2.cleaned_data['end_Date']
            user_id = form2.cleaned_data['employee_Choice']
            if user_id == "all":
                user_id = '%'

            def my_custom_sql():
                with connection.cursor() as cursor:
                    try:
                        row = ("Time Report Run At ", datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'),".","\n")
                        row += ("This report was run for the following dates: ", start, " through ", end, "." "\n")
                        if form.cleaned_data['report_Type'] == '1':
                            row += ("Employee Name","\t", " Time Type ", "\t", "Total Hours Logged, ","\t"," Number of Time Entries ", "\n")
                        else:
                            row += ("Employee Name, ", " Time Type, ", " Total Hours Logged, "," Number of Time Entries ", "\n")
                        cursor.execute("select concat(au.first_name, ' ', au.last_name), tt.timeType, CASE when tt.lunchin_time IS NULL AND tt.lunchout_time IS NULL THEN sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2)) WHEN tt.lunchin_time IS NULL and tt.lunchout_time IS NOT NULL THEN sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, DATE_SUB(tt.lunchout_time, INTERVAL 30 MINUTE), tt.lunchout_time)/60),2)) WHEN tt.lunchin_time IS NOT NULL and tt.lunchout_time IS NULL THEN sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, tt.lunchin_time, DATE_ADD(tt.lunchin_time, INTERVAL 30 MINUTE))/60),2)) ELSE sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, tt.lunchin_time, tt.lunchout_time)/60),2)) END, count(timeType) FROM times_timekeep tt JOIN auth_user au ON au.id = tt.user_id WHERE tt.in_time BETWEEN DATE_ADD(%s, INTERVAL 6 HOUR) AND DATE_ADD(%s, INTERVAL 30 HOUR) AND tt.user_id LIKE %s GROUP BY 1, 2", [start, end, user_id])
                        if form2.cleaned_data['report_Type'] == '1':
                            for rows in cursor.fetchall():
                                row += (rows[0], "\t ", rows[1], "\t     ", rows[2],"\t", "\t   ", rows[3], "\n")
                        else:
                            for rows in cursor.fetchall():
                                row += (rows[0],",", rows[1],",", rows[2],",", rows[3], "\n")
                        row += ("\n",)
                        row += ("The decimal is a percentage of an hour (ex .5 = 30minutes)",)
                    except:
                        row += ("There was an error while processing the request.",)
                    finally:
                        cursor.close()
                return row

            if form2.cleaned_data['report_Type'] == '1':          #### This is for web view. The else is for downloading file
                response = HttpResponse(my_custom_sql(), "")
                response['Content-Disposition'] = 'inline; filename="report.csv"'
            else:
                response = HttpResponse(my_custom_sql(), content_type='application/text charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="report.csv"'
            return response
        
    else:
        form = ReportForm()
        form2 = ReportselfForm()
        form3 = ReportTimePull()
    return render(request, 'reports.html', {'form': form, 'form2': form2, 'form3': form3})





    ################## This view for employee to pull only their own time. ########################
@login_required
def reportsUser_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = ReportUserForm(request.POST, user=request.user)
        form2 = ReportselfUserForm(request.POST, user=request.user)
        form3 = ReportTimeUserPull(request.POST, user=request.user)

        if form.is_valid() and 'predefined' in request.POST:
            time = form.cleaned_data['time_Frame']
            user_id = request.user.id

            def my_custom_sql():
                with connection.cursor() as cursor:
                    try:
                        row = ("Time Report Run At ", datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'),".","\n")
                        row += ("This report was run for the previous ", time, " days." "\n")
                        if form.cleaned_data['report_Type'] == '1':
                            row += ("Employee Name","\t","\t", " Time Type ", "\t","\t", "Total Hours Logged","\t","Number of Time Entries ", "\n")
                        else:
                            row += ("Employee Name, ", " Time Type, ", " Total Hours Logged, ","Number of Time Entries ", "\n")
                        cursor.execute("select concat(au.first_name, ' ', au.last_name), tt.timeType, CASE when tt.lunchin_time IS NULL AND tt.lunchout_time IS NULL THEN sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2)) WHEN tt.lunchin_time IS NULL and tt.lunchout_time IS NOT NULL THEN sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, DATE_SUB(tt.lunchout_time, INTERVAL 30 MINUTE), tt.lunchout_time)/60),2)) WHEN tt.lunchin_time IS NOT NULL and tt.lunchout_time IS NULL THEN sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, tt.lunchin_time, DATE_ADD(tt.lunchin_time, INTERVAL 30 MINUTE))/60),2)) ELSE sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, tt.lunchin_time, tt.lunchout_time)/60),2)) END, count(timeType) FROM times_timekeep tt JOIN auth_user au ON au.id = tt.user_id WHERE tt.in_time BETWEEN DATE_ADD(DATE_SUB(curdate(), INTERVAL %s DAY), INTERVAL 6 HOUR) AND date_add(curdate(), INTERVAL 30 HOUR) AND tt.user_id = %s GROUP BY 1, 2", [time, user_id])
                        if form.cleaned_data['report_Type'] == '1':
                            for rows in cursor.fetchall():
                                row += (rows[0],"\t ","\t", rows[1], "\t ","\t", rows[2], "\t ","\t", "\t ","\t", rows[3], "\n")
                        else:
                            for rows in cursor.fetchall():
                                row += (rows[0],",", rows[1],",", rows[2],",", rows[3], "\n")
                        row += ("\n",)
                        row += ("The decimal is a percentage of an hour (ex .5 = 30minutes)",)
                    except:
                        row += ("There was an error processing the report request. Please try again.",)
                    finally:
                        cursor.close()
                return row

            if form.cleaned_data['report_Type'] == '1':          #### This is for web view. The else is for downloading file
                response = HttpResponse(my_custom_sql(), "")
                response['Content-Disposition'] = 'inline; filename="report.csv"'
            else:
                response = HttpResponse(my_custom_sql(), content_type='application/text charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="report.csv"'
            return response

        elif form3.is_valid() and 'timeEntry' in request.POST:
            start = form3.cleaned_data['starting_Date']
            end = form3.cleaned_data['ending_Date']
            user_id = request.user.id
            dF = '%Y-%m-%d %H:%i'

            def my_custom_sql():
                with connection.cursor() as cursor:
                    try:
                        row = ("Time Report Run At ", datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'),".","\n")
                        row += ("This report was run for the following dates: ", start, " through ", end, "." "\n")
                        if form3.cleaned_data['report_Type'] == '1':
                            row += ("Employee Name    ", "Clocked In       ", "  Lunch Start "," Lunch End   ","Clocked Out ","\t", " Time Type      ", "Manual Entry", "\n")
                        else:
                            row += ("Employee Name, ", " Clocked In , ", " Lunch Start, "," Lunch End, "," Clocked Out , ", " Time Type, ", "Manual Entry", "\n")
                        cursor.execute("select concat(au.first_name, ' ', au.last_name), DATE_FORMAT(DATE_SUB(in_time, INTERVAL 6 HOUR), %s),DATE_FORMAT(DATE_SUB(lunchin_time, INTERVAL 6 HOUR), %s), DATE_FORMAT(DATE_SUB(lunchout_time, INTERVAL 6 HOUR), %s), DATE_FORMAT(DATE_SUB(out_time, INTERVAL 6 HOUR), %s), timeType, is_Manual FROM times_timekeep tt JOIN auth_user au ON au.id = tt.user_id WHERE tt.in_time BETWEEN DATE_ADD(%s, INTERVAL 6 HOUR) AND DATE_ADD(%s, INTERVAL 30 HOUR) AND tt.user_id = %s ORDER BY 2,1", [dF, dF, dF, dF, start, end, user_id])
                        if form3.cleaned_data['report_Type'] == '1':
                            for rows in cursor.fetchall():
                                if rows[6] == 0:
                                    row += (rows[0], "\t ",rows[1],"\t ",rows[2],"\t ",rows[3],"\t ", rows[4], "\t ",rows[5],"\t ","False", "\n")
                                else:
                                    row += (rows[0], "\t ",rows[1],"\t ",rows[2],"\t ",rows[3],"\t ", rows[4], "\t ",rows[5],"\t ","True", "\n")
                        else:
                            for rows in cursor.fetchall():
                                if rows[6] == 0:
                                    row += (rows[0], ",",rows[1],",",rows[2],",",rows[3],",", rows[4], ",",rows[5],",","False", "\n")
                                else:
                                    row += (rows[0], ",",rows[1],", ",rows[2],",",rows[3],",", rows[4], ", ",rows[5],",","True", "\n")
                        row += ("\n",)
                        row += ("The decimal is a percentage of an hour (ex .5 = 30minutes)",)
                    except:
                        row += ("There was an error while processing the request",)
                    finally:
                        cursor.close()
                return row

            if form3.cleaned_data['report_Type'] == '1':          #### This is for web view. The else is for downloading file
                response = HttpResponse(my_custom_sql(), "")
                response['Content-Disposition'] = 'inline; filename="report.csv"'
            else:
                response = HttpResponse(my_custom_sql(), content_type='application/text charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="report.csv"'
            return response

        elif form2.is_valid() and 'customSummary' in request.POST:
            start = form2.cleaned_data['start_Date']
            end = form2.cleaned_data['end_Date']
            user_id = request.user.id

            def my_custom_sql():
                with connection.cursor() as cursor:
                    try:
                        row = ("Time Report Run At ", datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'),".","\n")
                        row += ("This report was run for the following dates: ", start, " through ", end, "." "\n")
                        if form.cleaned_data['report_Type'] == '1':
                            row += ("Employee Name","\t", " Time Type ", "\t", "Total Hours Logged, ","\t"," Number of Time Entries ", "\n")
                        else:
                            row += ("Employee Name, ", " Time Type, ", " Total Hours Logged, "," Number of Time Entries ", "\n")
                        cursor.execute("select concat(au.first_name, ' ', au.last_name), tt.timeType, CASE when tt.lunchin_time IS NULL AND tt.lunchout_time IS NULL THEN sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2)) WHEN tt.lunchin_time IS NULL and tt.lunchout_time IS NOT NULL THEN sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, DATE_SUB(tt.lunchout_time, INTERVAL 30 MINUTE), tt.lunchout_time)/60),2)) WHEN tt.lunchin_time IS NOT NULL and tt.lunchout_time IS NULL THEN sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, tt.lunchin_time, DATE_ADD(tt.lunchin_time, INTERVAL 30 MINUTE))/60),2)) ELSE sum(TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, tt.lunchin_time, tt.lunchout_time)/60),2)) END, count(timeType) FROM times_timekeep tt JOIN auth_user au ON au.id = tt.user_id WHERE tt.in_time BETWEEN DATE_ADD(%s, INTERVAL 6 HOUR) AND DATE_ADD(%s, INTERVAL 30 HOUR) AND tt.user_id = %s GROUP BY 1, 2", [start, end, user_id])
                        if form2.cleaned_data['report_Type'] == '1':
                            for rows in cursor.fetchall():
                                row += (rows[0], "\t ", rows[1], "\t     ", rows[2],"\t", "\t   ", rows[3], "\n")
                        else:
                            for rows in cursor.fetchall():
                                row += (rows[0],",", rows[1],",", rows[2],",", rows[3], "\n")
                        row += ("\n",)
                        row += ("The decimal is a percentage of an hour (ex .5 = 30minutes)",)
                    except:
                        row += ("There was an error while processing the request.",)
                    finally:
                        cursor.close()
                return row

            if form2.cleaned_data['report_Type'] == '1':          #### This is for web view. The else is for downloading file
                response = HttpResponse(my_custom_sql(), "")
                response['Content-Disposition'] = 'inline; filename="report.csv"'
            else:
                response = HttpResponse(my_custom_sql(), content_type='application/text charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="report.csv"'
            return response
        
    else:
        form = ReportUserForm(user=request.user)
        form2 = ReportselfUserForm(user=request.user)
        form3 = ReportTimeUserPull(user=request.user)
    return render(request, 'reports.html', {'form': form, 'form2': form2, 'form3': form3})
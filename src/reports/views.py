from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required#, permission_required
from .forms import ReportForm,ReportselfForm, ReportTimePull, ReportUserForm, ReportselfUserForm, ReportTimeUserPull
from django.db import connection
from django.utils.timezone import datetime#, timedelta, now
# from django.utils import timezone, dateformat
# from times.models import timeKeep

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
                        row = ("Time Report Run At " + str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')) + ".","\n")
                        row += ("This report was run for the previous " + str(time) + " days." ,"\n")
                        if form.cleaned_data['report_Type'] == '1':
                            row += ("<th>Employee Name</th><th>Time Type</th><th>Total Hours Logged</th><th>Number of Time Entries" ,)
                        else:
                            row += ("Employee Name, ", " Time Type, ", " Total Hours Logged, "," Number of Time Entries ","\n")
                        cursor.execute("select concat(au.first_name, ' ', au.last_name), tt.timeType,sum(IF(lunchin_time IS NULL AND lunchout_time IS NULL, TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2), TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, tt.lunchin_time, tt.lunchout_time)/60),2))), count(timeType) FROM times_timekeep tt JOIN auth_user au ON au.id = tt.user_id WHERE tt.in_time BETWEEN DATE_ADD(DATE_SUB(curdate(), INTERVAL %s DAY), INTERVAL 6 HOUR) AND date_add(curdate(), INTERVAL 30 HOUR) AND tt.user_id LIKE %s GROUP BY 1, 2", [time, user_id])
                        if form.cleaned_data['report_Type'] == '1':
                            for rows in cursor.fetchall():
                                row += ("<td>" + str(rows[0]) + "</td>" + "<td>" + str(rows[1]) + "</td>" + "<td>" + str(rows[2]) + "</td>" + "<td>" + str(rows[3]) + "</td>",)
                        else:
                            for rows in cursor.fetchall():
                                row += (rows[0],",", rows[1],",", rows[2],",", rows[3], "\n")
                            row += ("\n",)
                        row += ("The decimal is a percentage of an hour (ex .5 = 30minutes).",)
                        row += ("Please press the back arrow in your browser to return to the application.",)
                    except Exception as e:
                        row += ("There was an error while processing the request." + "error: " + str(e),)
                    finally:
                        cursor.close()
                return row

            if form.cleaned_data['report_Type'] == '1':          #### This is for web view. The else is for downloading file
                response = my_custom_sql()
                table = "<table><style> table { width: 60%; padding-left: 50px; text-align: center;}</style>"
                for rows in response:
                    table += "<tr> {} </tr>".format(rows)
                table += "</table>"
                response = HttpResponse(table)

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
                        row = ("Time Report Run At " + str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')) + ".","\n")
                        row += ("This report was run for the following dates: " + str(start) + " through " + str(end) + ".", "\n")
                        if form3.cleaned_data['report_Type'] == '1':
                            row += ("<th>Employee Name</th><th>Clocked In</th><th>Lunch Start</th><th>Lunch End</th><th>Clocked Out</th><th>Time Type</th><th>Manual Entry</th>", "\n")
                        else:
                            row += ("Employee Name, ", " Clocked In , ", " Lunch Start, "," Lunch End, "," Clocked Out , ", " Time Type, ", "Manual Entry", "\n")
                        cursor.execute("select concat(au.first_name, ' ', au.last_name), DATE_FORMAT(DATE_SUB(in_time, INTERVAL 6 HOUR), %s),DATE_FORMAT(DATE_SUB(lunchin_time, INTERVAL 6 HOUR), %s), DATE_FORMAT(DATE_SUB(lunchout_time, INTERVAL 6 HOUR), %s), DATE_FORMAT(DATE_SUB(out_time, INTERVAL 6 HOUR), %s), timeType, is_Manual FROM times_timekeep tt JOIN auth_user au ON au.id = tt.user_id WHERE tt.in_time BETWEEN DATE_ADD(%s, INTERVAL 6 HOUR) AND DATE_ADD(%s, INTERVAL 30 HOUR) AND tt.user_id LIKE %s ORDER BY 2,1", [dF, dF, dF, dF, start, end, user_id])
                        if form3.cleaned_data['report_Type'] == '1':
                            for rows in cursor.fetchall():
                                if rows[6] == 0:
                                    row += ("<td>" + str(rows[0]) + "</td>" + "<td>" + str(rows[1])+ "</td>" + "<td>" + str(rows[2]) + "</td>" + "<td>" + str(rows[3]) + "</td>" + "<td>" + str(rows[4]) + "</td>" + "<td>" + str(rows[5]) + "</td>" + "<td>" + "False" + "</td>", "\n")
                                else:
                                    row += ("<td>" + str(rows[0]) + "</td>" + "<td>" + str(rows[1])+ "</td>" + "<td>" + str(rows[2]) + "</td>" + "<td>" + str(rows[3]) + "</td>" + "<td>" + str(rows[4]) + "</td>" + "<td>" + str(rows[5]) + "</td>" + "<td>" + "True" + "</td>", "\n")
                        else:
                            for rows in cursor.fetchall():
                                if rows[6] == 0:
                                    row += (rows[0], ",",rows[1],",",rows[2],",",rows[3],",", rows[4], ",",rows[5],",","False", "\n")
                                else:
                                    row += (rows[0], ",",rows[1],", ",rows[2],",",rows[3],",", rows[4], ", ",rows[5],",","True", "\n")
                        row += ("\n",)
                        row += ("The decimal is a percentage of an hour (ex .5 = 30minutes).",)
                        row += ("Please press the back arrow in your browser to return to the application.",)
                    except Exception as e:
                        row += ("There was an error while processing the request." + "error: " + str(e),)
                    finally:
                        cursor.close()
                return row

            if form3.cleaned_data['report_Type'] == '1':          #### This is for web view. The else is for downloading file
                response = my_custom_sql()
                table = "<table><style> table { width: 80%; padding-left: 50px; text-align: center;}</style>"
                for rows in response:
                    table += "<tr> {} </tr>".format(rows)
                table += "</table>"
                response = HttpResponse(table)
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
                        row = ("Time Report Run At " + str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')) + ".","\n")
                        row += ("This report was run for the following dates: " + str(start) + " through " + str(end) + ".", "\n")
                        if form.cleaned_data['report_Type'] == '1':
                            row += ("<th>Employee Name</th><th>Time Type</th><th>Total Hours Logged</th><th>Number of Time Entries</th>", "\n")
                        else:
                            row += ("Employee Name, ", " Time Type, ", " Total Hours Logged, "," Number of Time Entries ", "\n")
                        cursor.execute("select concat(au.first_name, ' ', au.last_name), tt.timeType,sum(IF(lunchin_time IS NULL AND lunchout_time IS NULL, TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2), TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, tt.lunchin_time, tt.lunchout_time)/60),2))), count(timeType) FROM times_timekeep tt, auth_user au WHERE au.id = tt.user_id AND tt.in_time BETWEEN DATE_ADD(DATE_SUB(curdate(), INTERVAL %s DAY), INTERVAL 6 HOUR) AND date_add(%s, INTERVAL 30 HOUR) AND tt.user_id LIKE %s GROUP BY 1,2", [start, end, user_id])
                        if form2.cleaned_data['report_Type'] == '1':
                            for rows in cursor.fetchall():
                                row += ("<td>" + str(rows[0]) + "</td>" + "<td>" + str(rows[1]) + "</td>" + "<td>" + str(rows[2]) + "</td>" + "<td>" + str(rows[3]) + "</td>",  "\n")
                        else:
                            for rows in cursor.fetchall():
                                row += (rows[0],",", rows[1],",", rows[2],",", rows[3], "\n")
                        row += ("\n",)
                        row += ("The decimal is a percentage of an hour (ex .5 = 30minutes).",)
                        row += ("Please press the back arrow in your browser to return to the application.",)
                    except Exception as e:
                        row += ("There was an error while processing the request." + "error: " + str(e),)
                    finally:
                        cursor.close()
                return row

            if form2.cleaned_data['report_Type'] == '1':          #### This is for web view. The else is for downloading file
                response = my_custom_sql()
                table = "<table><style> table { width: 60%; text-align: center;}</style>"
                for rows in response:
                    table += "<tr> {} </tr>".format(rows)
                table += "</table>"
                response = HttpResponse(table)
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
        form = ReportUserForm(request.POST)
        form2 = ReportselfUserForm(request.POST)
        form3 = ReportTimeUserPull(request.POST)

        if form.is_valid() and 'predefined' in request.POST:
            time = form.cleaned_data['time_Frame']
            user_id = request.user.id


            def my_custom_sql():
                with connection.cursor() as cursor:
                    try:
                        row = ("Time Report Run At " + str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')) + ".","\n")
                        row += ("This report was run for the previous " + str(time) + " days." ,"\n")
                        if form.cleaned_data['report_Type'] == '1':
                            row += ("<th>Employee Name</th><th>Time Type</th><th>Total Hours Logged</th><th>Number of Time Entries" ,)
                        else:
                            row += ("Employee Name, ", " Time Type, ", " Total Hours Logged, "," Number of Time Entries ","\n")
                        cursor.execute("select concat(au.first_name, ' ', au.last_name), tt.timeType,sum(IF(lunchin_time IS NULL AND lunchout_time IS NULL, TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2), TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, tt.lunchin_time, tt.lunchout_time)/60),2))), count(timeType) FROM times_timekeep tt JOIN auth_user au ON au.id = tt.user_id WHERE tt.in_time BETWEEN DATE_ADD(DATE_SUB(curdate(), INTERVAL %s DAY), INTERVAL 6 HOUR) AND date_add(curdate(), INTERVAL 30 HOUR) AND tt.user_id = %s GROUP BY 1, 2", [time, user_id])
                        if form.cleaned_data['report_Type'] == '1':
                            for rows in cursor.fetchall():
                                row += ("<td>" + str(rows[0]) + "</td>" + "<td>" + str(rows[1]) + "</td>" + "<td>" + str(rows[2]) + "</td>" + "<td>" + str(rows[3]) + "</td>",)
                        else:
                            for rows in cursor.fetchall():
                                row += (rows[0],",", rows[1],",", rows[2],",", rows[3], "\n")
                            row += ("\n",)
                        row += ("The decimal is a percentage of an hour (ex .5 = 30minutes).",)
                        row += ("Please press the back arrow in your browser to return to the application.",)
                    except Exception as e:
                        row += ("There was an error while processing the request." + "error: " + str(e),)
                    finally:
                        cursor.close()
                return row

            if form.cleaned_data['report_Type'] == '1':          #### This is for web view. The else is for downloading file
                response = my_custom_sql()
                table = "<table><style> table { width: 60%; padding-left: 50px; text-align: center;}</style>"
                for rows in response:
                    table += "<tr> {} </tr>".format(rows)
                table += "</table>"
                response = HttpResponse(table)

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
                        row = ("Time Report Run At " + str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')) + ".","\n")
                        row += ("This report was run for the following dates: " + str(start) + " through " + str(end) + ".", "\n")
                        if form3.cleaned_data['report_Type'] == '1':
                            row += ("<th>Employee Name</th><th>Clocked In</th><th>Lunch Start</th><th>Lunch End</th><th>Clocked Out</th><th>Time Type</th><th>Manual Entry</th>", "\n")
                        else:
                            row += ("Employee Name, ", " Clocked In , ", " Lunch Start, "," Lunch End, "," Clocked Out , ", " Time Type, ", "Manual Entry", "\n")
                        cursor.execute("select concat(au.first_name, ' ', au.last_name), DATE_FORMAT(DATE_SUB(in_time, INTERVAL 6 HOUR), %s),DATE_FORMAT(DATE_SUB(lunchin_time, INTERVAL 6 HOUR), %s), DATE_FORMAT(DATE_SUB(lunchout_time, INTERVAL 6 HOUR), %s), DATE_FORMAT(DATE_SUB(out_time, INTERVAL 6 HOUR), %s), timeType, is_Manual FROM times_timekeep tt JOIN auth_user au ON au.id = tt.user_id WHERE tt.in_time BETWEEN DATE_ADD(%s, INTERVAL 6 HOUR) AND DATE_ADD(%s, INTERVAL 30 HOUR) AND tt.user_id = %s ORDER BY 2,1", [dF, dF, dF, dF, start, end, user_id])
                        if form3.cleaned_data['report_Type'] == '1':
                            for rows in cursor.fetchall():
                                if rows[6] == 0:
                                    row += ("<td>" + str(rows[0]) + "</td>" + "<td>" + str(rows[1])+ "</td>" + "<td>" + str(rows[2]) + "</td>" + "<td>" + str(rows[3]) + "</td>" + "<td>" + str(rows[4]) + "</td>" + "<td>" + str(rows[5]) + "</td>" + "<td>" + "False" + "</td>", "\n")
                                else:
                                    row += ("<td>" + str(rows[0]) + "</td>" + "<td>" + str(rows[1])+ "</td>" + "<td>" + str(rows[2]) + "</td>" + "<td>" + str(rows[3]) + "</td>" + "<td>" + str(rows[4]) + "</td>" + "<td>" + str(rows[5]) + "</td>" + "<td>" + "True" + "</td>", "\n")
                        else:
                            for rows in cursor.fetchall():
                                if rows[6] == 0:
                                    row += (rows[0], ",",rows[1],",",rows[2],",",rows[3],",", rows[4], ",",rows[5],",","False", "\n")
                                else:
                                    row += (rows[0], ",",rows[1],", ",rows[2],",",rows[3],",", rows[4], ", ",rows[5],",","True", "\n")
                        row += ("\n",)
                        row += ("The decimal is a percentage of an hour (ex .5 = 30minutes).",)
                        row += ("Please press the back arrow in your browser to return to the application.",)
                    except Exception as e:
                        row += ("There was an error while processing the request." + "error: " + str(e),)
                    finally:
                        cursor.close()
                return row

            if form3.cleaned_data['report_Type'] == '1':          #### This is for web view. The else is for downloading file
                response = my_custom_sql()
                table = "<table><style> table { width: 80%; padding-left: 50px; text-align: center;}</style>"
                for rows in response:
                    table += "<tr> {} </tr>".format(rows)
                table += "</table>"
                response = HttpResponse(table)
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
                        row = ("Time Report Run At " + str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M')) + ".","\n")
                        row += ("This report was run for the following dates: " + str(start) + " through " + str(end) + ".", "\n")
                        if form.cleaned_data['report_Type'] == '1':
                            row += ("<th>Employee Name</th><th>Time Type</th><th>Total Hours Logged</th><th>Number of Time Entries</th>", "\n")
                        else:
                            row += ("Employee Name, ", " Time Type, ", " Total Hours Logged, "," Number of Time Entries ", "\n")
                        cursor.execute("select concat(au.first_name, ' ', au.last_name), tt.timeType,sum(IF(lunchin_time IS NULL AND lunchout_time IS NULL, TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2), TRUNCATE((timestampdiff(MINUTE, in_time, out_time)/60),2) - TRUNCATE((timestampdiff(MINUTE, tt.lunchin_time, tt.lunchout_time)/60),2))), count(timeType) FROM times_timekeep tt JOIN auth_user au ON au.id = tt.user_id WHERE tt.in_time BETWEEN DATE_ADD(%s, INTERVAL 6 HOUR) AND DATE_ADD(%s, INTERVAL 30 HOUR) AND tt.user_id LIKE %s GROUP BY 1, 2", [start, end, user_id])
                        if form2.cleaned_data['report_Type'] == '1':
                            for rows in cursor.fetchall():
                                row += ("<td>" + str(rows[0]) + "</td>" + "<td>" + str(rows[1]) + "</td>" + "<td>" + str(rows[2]) + "</td>" + "<td>" + str(rows[3]) + "</td>",  "\n")
                        else:
                            for rows in cursor.fetchall():
                                row += (rows[0],",", rows[1],",", rows[2],",", rows[3], "\n")
                        row += ("\n",)
                        row += ("The decimal is a percentage of an hour (ex .5 = 30minutes).",)
                        row += ("Please press the back arrow in your browser to return to the application.",)
                    except Exception as e:
                        row += ("There was an error while processing the request." + "error: " + str(e),)
                    finally:
                        cursor.close()
                return row

            if form2.cleaned_data['report_Type'] == '1':          #### This is for web view. The else is for downloading file
                response = my_custom_sql()
                table = "<table><style> table { width: 60%; text-align: center;}</style>"
                for rows in response:
                    table += "<tr> {} </tr>".format(rows)
                table += "</table>"
                response = HttpResponse(table)
            else:
                response = HttpResponse(my_custom_sql(), content_type='application/text charset=utf-8')
                response['Content-Disposition'] = 'attachment; filename="report.csv"'
            return response

    else:
        form = ReportUserForm()
        form2 = ReportselfUserForm()
        form3 = ReportTimeUserPull()
    return render(request, 'reports.html', {'form': form, 'form2': form2, 'form3': form3})



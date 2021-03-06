"""timecard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.contrib.auth import urls

#from pages.views import signon_view
from times.views import timeEntry_view, timeEdit_view
from reports.views import reports_view, reportsUser_view
from profiles.views import profileCreation_view, requests_view
from pages.views import redirect_login, change_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reports/', reports_view, name='reports'),
    path('timeEntry/', timeEntry_view, name='timeEntry'),
    path('profileCreation/', profileCreation_view, name='profileCreation'),
    path('requests/', requests_view, name='requests'),
    path('timeEdit/', timeEdit_view,name='timeEdit'),
    path('', redirect_login, name='redirect'),
    path('change_password', change_password, name ='change_password'),
    path('userReports/', reportsUser_view, name='userReports')
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

admin.site.site_header = "Medical Office Online Timecard Admin"
admin.site.site_title = "Medical Office Online Timecard Admin Portal"
admin.site.index_title = "Welcome to Medical Office Online Timecard Portal"
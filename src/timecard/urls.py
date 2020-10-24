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

#from pages.views import signon_view
from times.views import timeEntry_view
from reports.views import reports_view
from profiles.views import profileCreation_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reports/', reports_view, name='reports'),
    path('timeEntry/', timeEntry_view, name='timeEntry'),
    path('profileCreation/', profileCreation_view, name='profileCreation')
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

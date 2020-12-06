from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Request, User
from .forms import ProfileForm, RequestForm
from . import models, forms
import re
from django.utils.timezone import timedelta, now

# Register your models here.

class requestAdmin(admin.ModelAdmin):
    list_display = ['user','request_Type','status','start_Date_Time','end_Date_Time']
    list_per_page = 10
    readonly_fields = ["user"]
    model = models.Request

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        def get_queryset(self, request):
            qs = super().get_queryset(request)
            return qs
        x = request.META['PATH_INFO']
        try:
            y = int(re.search(r'\d+', x).group())
            obj = get_queryset(self, request).get(id=y)
            if obj.status == "Approved":
                return False
            else:
                return True
        except:
            return True

    def has_delete_permission(self, request, obj=None):
        return True

class CustomUserAdmin(UserAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser == True:
            def get_queryset(self, request):
                qs = super().get_queryset(request)
                return qs
            x = request.META['PATH_INFO']
            try:
                days_sub = timedelta(days=30)
                y = int(re.search(r'\d+', x).group())
                obj = get_queryset(self, request).get(id=y)
                if obj.is_active == True:
                    return False
                elif obj.last_login == None:
                    return True
                elif (obj.last_login > now() - days_sub):
                    return False
                else:
                    return True
            except:
                return False
        else:
            return False

class profileAdmin(admin.ModelAdmin):
    list_per_page = 10
    form = ProfileForm
    model = models.Profile
    readonly_fields = ["user"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile,profileAdmin)
admin.site.register(Request,requestAdmin)

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
    def render_change_form(self, request, context, *args, **kwargs):
        # here we define a custom template
        self.change_form_template = 'admin/change_form_help_text.html'
        extra = {
            'help_text': "This form is for viewing/adjusting employee requests. Here PTO, Sick Day, Overtime, and Time Correction Requests are displayed. Requests are initially marked as 'Requested'. Upon marking a request as 'Approved' the proper entry will be made to the time table and if necessary deduct PTO/Sick time hours accordingly. "
        }

        context.update(extra)
        return super(requestAdmin, self).render_change_form(request,
            context, *args, **kwargs)


    list_display = ['user','request_Type','status','start_Date_Time','end_Date_Time']
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
    )

    list_per_page = 10
    readonly_fields = ["user", 'submission_Date']
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

    def render_change_form(self, request, context, *args, **kwargs):
        # here we define a custom template
        self.change_form_template = 'admin/change_form_help_text.html'
        extra = {
            'help_text': "On this page you have individual access to view/edit a user's profile. Supervisors and management are able to change passwords of users should they forget, edit personal information such as name and email, and assign custom permissions through predefined groups."
        }

        context.update(extra)
        return super(CustomUserAdmin, self).render_change_form(request,
            context, *args, **kwargs)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser == True:
            return True
        else:
            return False

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

    def render_change_form(self, request, context, *args, **kwargs):
        # here we define a custom template
        self.change_form_template = 'admin/change_form_help_text.html'
        extra = {
            'help_text': "This form is for viewing/adjusting employee profile attributes. Here PTO, Sick Day, PTO Bi-Weekly Accrual Rate, and Sick Time Bi-Weekly Accrual Rate are displayed in hours. The decimal is a percentage of an hour (ex. .5 = 30min)."
        }

        context.update(extra)
        return super(profileAdmin, self).render_change_form(request,
            context, *args, **kwargs)

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
                user = User.objects.get(id=y)
                if user.is_active == True:
                    return False
                elif user.last_login == None:
                    return True
                elif (user.last_login > now() - days_sub):
                    return False
                else:
                    return True
            except:
                return False
        else:
            return False

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile,profileAdmin)
admin.site.register(Request,requestAdmin)

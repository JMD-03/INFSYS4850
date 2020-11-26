from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Request, User
from .forms import ProfileForm
from . import models
from times.models import timeKeep

# Register your models here.

class requestAdmin(admin.ModelAdmin):
    list_display = ['user','request_Type','status','start_Date_Time','end_Date_Time']
    list_per_page = 10
    readonly_fields = ["user"]
    model = models.Request
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

class CustomUserAdmin(UserAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
            return True

class profileAdmin(admin.ModelAdmin):
    #list_display = ['user']
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




# class CustomUserAdmin(UserAdmin):

#     def has_delete_permission(self, request, obj=None):  # note the obj=None
#         return True

#         #Needs edit, this is straight from stack overflow
#     def __init__(self, *args, **kwargs):
#         super(UserAdmin, self).__init__(*args, **kwargs)
#         UserAdmin.list_display = list(UserAdmin.list_display) #+ ['date_joined', 'some_function']
#         print(User)
#         print(UserAdmin.list_display)
#         queryset = timeKeep.objects.filter(user=request.user)
#         print(queryset)
#     # # Function to count objects of each user from another Model (where user is FK)
#     # def some_function(self, obj):
#     #     return obj.another_model_set.count()


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile,profileAdmin)
admin.site.register(Request,requestAdmin)

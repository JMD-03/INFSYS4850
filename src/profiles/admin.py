from django.contrib import admin
from .models import Profile, Request

# Register your models here.

class requestAdmin(admin.ModelAdmin):
    list_display = ['user','request_Type']
    list_per_page = 10

admin.site.register(Profile)
admin.site.register(Request,requestAdmin)

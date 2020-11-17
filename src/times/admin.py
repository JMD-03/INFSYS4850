from django.contrib import admin
from times.models import timeKeep

# Register your models here.


class timesAdmin(admin.ModelAdmin):
    list_display = ['user', 'in_time', 'out_time']
    list_per_page = 10

admin.site.register(timeKeep, timesAdmin)
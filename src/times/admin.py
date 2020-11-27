from django.contrib import admin
from times.models import timeKeep

# Register your models here.


class timesAdmin(admin.ModelAdmin):
    list_display = ['user', 'in_time', 'out_time']
    list_per_page = 10
    readonly_fields = [ "clocked_in"]
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
admin.site.register(timeKeep, timesAdmin)
from django.contrib import admin
from times.models import timeKeep

# Register your models here.


class timesAdmin(admin.ModelAdmin):

    def render_change_form(self, request, context, *args, **kwargs):
        # here we define a custom template
        self.change_form_template = 'admin/change_form_help_text.html'
        extra = {
            'help_text': "On this page you have access to see/edit individual time entries made by users. Supervisors and management are able to change entries of users should they notice a mistake. Requests that are approved will update this screen accordingly with new or updated time entries."
        }

        context.update(extra)
        return super(timesAdmin, self).render_change_form(request,
            context, *args, **kwargs)

    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
    )

    list_display = ['user', 'in_time', 'out_time','timeType']
    list_per_page = 10
    readonly_fields = ['user', 'dateTimeEntered','clocked_in','is_Manual']
    def has_add_permission(self, request, obj=None):
        return False

    # def has_change_permission(self, request, obj=None):
    #     return True

    # def has_delete_permission(self, request, obj=None):
    #     return True


admin.site.register(timeKeep, timesAdmin)
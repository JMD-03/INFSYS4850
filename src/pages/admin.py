from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
class GroupsAdmin(admin.ModelAdmin):
    # list_display = ["name", "pk"]
    # class Meta:
    #     model = Group

    def render_change_form(self, request, context, *args, **kwargs):
        # here we define a custom template
        self.change_form_template = 'admin/change_form_help_text.html'
        extra = {
            'help_text': "This form is for viewing/adjusting group level permissions. Here supervisors can view and managers can edit group permissions. Managers may also create new custom groups and define their attributes."
        }

        context.update(extra)
        return super(GroupsAdmin, self).render_change_form(request,
            context, *args, **kwargs)


admin.site.unregister(Group)
admin.site.register(Group, GroupsAdmin)
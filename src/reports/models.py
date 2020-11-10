from django.db import models

# Create your models here.

class RightsSupport(models.Model):

    class Meta:

        managed = False  # No database table creation or deletion  \
        # operations will be performed for this model.

        # default_permissions = ("view")  # disable "add", "change", "delete"
        # # and "view" default permissions

        permissions = (
            ('employee_view', 'Global Employee View'),
            ('supervisor_view', 'Global supervisor view'),
            ('management_view', 'Global management view'),
        )

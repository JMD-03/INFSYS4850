from django.db import models
from django.contrib.auth.models import User
from django.utils import datetime

# Create your models here.
class timekeep(models.Model):
    user = models.ForeignKey(User) #This will actually be blank=false
    c_in = models.DateTimeField(datetime.now()) #will actually be blank=false
    c_out = models.DateTimeField(null = true, blank = false)
    clocked = models.BooleanField(default=true)

    #when the clock in button is pushed
    def clocked_in(self):
        self.clocked = True
        self.save()
        #when the clock out button is pushed
        def clocked_out(self):
            self.c_out = timezone.now()
            self.clocked = False
            self.save()

            class Meta:
                get_latest_by = clocked
                ordering = ['-in_time']
                #verbose_name = table name
                #verbose_name_plural = table name plural


from django.contrib import admin
from .models import Event, Attendance, EventSession

# Register your models here.
admin.site.register([Attendance,Event,EventSession])

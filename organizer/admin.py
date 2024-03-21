from django.contrib import admin
from .models import Organizer, Events

# Register your models here.
admin.site.register([Events,Organizer])

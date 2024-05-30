import pytz
import datetime

from django.db import models
from django.utils.timezone import now
from api.models import SatsUser # Create your models here.

class Event(models.Model):
	EVENT_TYPE_CHOICES = (
		('One off', 'One off'),
		('Recurring', 'Recurring'),
	)
	
	EVENT_ACCESS_CHOICES = (
		('Public', 'public'),
		('On-Register', 'on_register'),
		('Restricted', 'restricted')
	)

	TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]

	name = models.TextField()
	event_type = models.TextField(max_length=15,choices=EVENT_TYPE_CHOICES)
	venue = models.TextField()
	reward = models.IntegerField()
	timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES)
	created_at = models.DateTimeField(auto_now_add=True)
	access = models.CharField(max_length=30, choices=EVENT_ACCESS_CHOICES)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.created_at = datetime.datetime.today() 
		self.created_at = self.created_at.astimezone(pytz.timezone(self.timezone)) 
		super(Event, self).save(*args, **kwargs)



class EventSession(models.Model):
	title = models.TextField()
	parent_event = models.ForeignKey(Event,on_delete=models.CASCADE)
	deadline = models.DateTimeField()
	def __str__(self):
		return f"ID: {self.pk} - Name: {self.title}"
	
	def save(self, *args, **kwargs):
		parent_timezone = self.parent_event.timezone
		self.deadline = self.deadline.astimezone(pytz.timezone(parent_timezone))
		super(EventSession, self).save(*args, **kwargs)
		


	@classmethod
	def get_method(cls,**kwargs):
		return cls.objects.filter(**kwargs).prefetch_related(
            models.Prefetch('eventSessions', queryset=EventSession.objects.all()),  # Renamed eventsession_set to eventSessions
            models.Prefetch('attendance', queryset=Attendance.objects.select_related('user'))  # Renamed attendance_set to attendance
        )

class Attendance(models.Model):
	first_name = models.TextField(default="")
	last_name = models.TextField(default="")
	employee_id = models.TextField(default="")
	user = models.ForeignKey(SatsUser, on_delete=models.CASCADE)
	eventSession = models.ForeignKey(EventSession, on_delete=models.CASCADE)
	is_activated = models.BooleanField(default=False)
	clock_in_time = models.DateTimeField(auto_now_add=True)

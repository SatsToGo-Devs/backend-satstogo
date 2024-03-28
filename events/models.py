from django.db import models
from api.models import User
from datetime import datetime
# Create your models here.

class Event(models.Model):
	EVENT_TYPE_CHOICES = (
		('One off', 'One off'),
		('Recurring', 'Recurring'),
	)
	name = models.TextField()
	deadline = models.DateTimeField()
	event_type = models.TextField(max_length=15,choices=EVENT_TYPE_CHOICES)
	venue = models.TextField()
	reward = models.IntegerField()
	def __str__(self):
		return self.name

class EventSession(models.Model):
	title = models.TextField()
	parent_event = models.ForeignKey(Event,on_delete=models.CASCADE)
	deadline = models.DateTimeField()

	def __str__(self):
		return f"ID: {self.pk} - Name: {self.title}"


class Attendance(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	event = models.ForeignKey(EventSession, on_delete=models.CASCADE)
	is_activated = models.BooleanField(default=False)
	clock_in_time = models.DateTimeField(auto_now_add=True)


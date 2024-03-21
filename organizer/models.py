from django.db import models
# Create your models here.


class Organizer(models.Model):
	name = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	is_business = models.BooleanField(default=True)

	def __str__(self):
		return self.name


class Events(models.Model):
	EVENT_TYPE_CHOICES = (
		(1, 'Admin'),
		(2, 'Staff'),
		(3, 'Customer')
	)
	organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
	name = models.TextField()
	deadline = models.DateField()
	event_type = models.CharField(max_length=10,choices=EVENT_TYPE_CHOICES)
	venue = models.TextField()

	def __str__(self):
		return self.name



class EventSession(models.Model):
	title = models.TextField()
	parent_event = models.ForeignKey(Events,on_delete=models.CASCADE)

	def __str__(self):
		return self.title





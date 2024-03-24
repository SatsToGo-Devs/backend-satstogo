from django.db import models
from django.utils import timezone
# Create your models here.

class User(models.Model):
	magic_string = models.TextField()
	key = models.TextField()
	sig = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Magic: {self.magic_string}, last_login: {self.last_login}"
	
	def update_last_login(self):
		self.last_login = timezone.now()
		self.save(update_fields=['last_login'])

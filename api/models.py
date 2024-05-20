from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.exceptions import ValidationError

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, magic_string, key, sig, **extra_fields):
        """
        Create a regular user without a username or password.
        """
        if not magic_string:
            raise ValueError("Magic string is required for user creation.")
        user = self.model(magic_string=magic_string,username=magic_string,key=key, sig=sig, **extra_fields)
        user.set_unusable_password()  # Set an unusable password
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create a superuser with an email and password.
        """
        if not username:
            raise ValueError("Username is required for superuser creation.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser):
	magic_string = models.TextField(unique=True)
	key = models.TextField()
	sig = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_superuser = models.BooleanField(default=False)

	REQUIRED_FIELDS = ['username']

	objects = CustomUserManager()


	USERNAME_FIELD = 'magic_string'

	def __str__(self):
		return f"Magic: {self.magic_string}, last_login: {self.last_login}"

	def update_last_login(self):
		self.last_login = timezone.now()
		self.save(update_fields=['last_login'])

class SatsUser(models.Model):
	magic_string = models.TextField(unique=True)
	key = models.TextField()
	sig = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"magic_string: {self.magic_string},key: {self.key},sig: {self.sig},created_at: {self.created_at}, last_login: {self.last_login}"

	def update_last_login(self):
		self.last_login = timezone.now()
		self.save(update_fields=['last_login'])

class FcmToken(models.Model):
	magic_string = models.TextField(unique=True)
	token = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"magic_string: {self.magic_string},token: {self.token},created_at: {self.created_at}"

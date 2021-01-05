from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager

class User(AbstractUser):
	username = None
	email = models.EmailField(_('Email address'), max_length=64, unique=True)
	first_name = models.CharField(max_length=64)
	last_name = models.CharField(max_length=64)
	is_student = models.BooleanField('Student status', default=True)
	is_teacher = models.BooleanField('Teacher status', default=False)
	is_active = models.BooleanField('User account status', default=True, blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	objects = UserManager()

	def __str__(self):
		return self.email

class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Teacher(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)



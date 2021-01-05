import datetime

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField()
	parent = models.ForeignKey('self', blank=True, on_delete=models.SET_NULL, null=True, related_name='children')

	class Meta:
		unique_together = ('slug', 'parent',)
		verbose_name_plural = "categories"   

	def __str__(self):                           
		return self.name

class Course(models.Model):
	slug = models.SlugField()
	title = models.CharField(max_length=120)
	description = models.TextField(default="", blank=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Course, self).save(*args, **kwargs)


class Lesson(models.Model):
	slug = models.SlugField()
	title = models.CharField(max_length=200)
	item = models.IntegerField()
	course = models.ManyToManyField(Course, blank=True, related_name='lessons')
	position = models.IntegerField()

	def __str__(self):
		return self.slug


class Slide(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField()
	lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, related_name='slides')
	position = models.IntegerField()
	content = models.TextField()

	def __str__(self):
		return self.title
from django.db import models

from django.contrib.auth.models import User


class QuestionManager(models.Manager):
	def new(self):
		return self.order_by('-added_at')[0:20]
	def popular(self):
		return self.order_by('rating')


class Question(models.Model):
	title = models.CharField(max_length=255)
	text = models.TextField()
	added_at = models.DateField()
	rating = models.IntegerField(default=0)
	author = models.ForeignKey(User)
	likes = models.ManyToManyField(User)


class Answer(models.Model):
	text = models.TextField()
	added_at = models.DateField()
	question = models.ForeignKey(Question)
	author = models.ForeignKey(User)

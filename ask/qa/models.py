from django.db import models

from django.contrib.auth.models import User

from django.core.urlresolvers import reverse


class QuestionManager(models.Manager):
	def new(self):
		return self.order_by('-added_at')
	def popular(self):
		return self.order_by('-rating')


class Question(models.Model):
	objects = QuestionManager()
	title = models.CharField(max_length=255)
	text = models.TextField()
	added_at = models.DateField(auto_now_add=False)
	rating = models.IntegerField(default=0)
	author = models.ForeignKey(User, related_name='author')
	likes = models.ManyToManyField(User, related_name='likes')

	def __str__(self):
		return self.title

	def get_url(self):
		return reverse('one_question', kwargs = {'question_id': self.id})

	class Meta:
		ordering = ['id']


class Answer(models.Model):
	text = models.TextField()
	added_at = models.DateField(auto_now_add=False)
	question = models.ForeignKey(Question)
	author = models.ForeignKey(User)

	def __str__(self):
		return self.text

	class Meta:
		ordering = ['id']

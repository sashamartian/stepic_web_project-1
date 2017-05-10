from django.db import models

from django.contrib.auth.models import User

from django.core.urlresolvers import reverse


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-id')

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    objects = QuestionManager()
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, related_name='questions_is_author', default='1')
    likes = models.ManyToManyField(User, related_name='questions_likes', blank=True)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('one_question', kwargs={'question_id': self.id})


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateField(auto_now_add=True)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User, default='1')

    def __str__(self):
        return self.text

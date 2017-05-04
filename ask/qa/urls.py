from django.conf.urls import url

from .views import one_question

urlpatterns = [
    url(r'^(?P<question_id>\d+)/$', one_question, name='one_question')
]

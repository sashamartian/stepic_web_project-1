from django import forms

from .models import Answer, Question


class AskForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.Textarea)
    text = forms.CharField(widget=forms.Textarea)

    def save(self):
        question = Question(**self.cleaned_data)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.ModelChoiceField(queryset=Question.objects.all(), widget=forms.HiddenInput)

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer

from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Answer, Question


class AskForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.Textarea)
    text = forms.CharField(max_length=5000, required=False, widget=forms.Textarea)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super().__init__(*args, **kwargs)

    def save(self):
        self.cleaned_data['author'] = self._user
        return Question.objects.create(**self.cleaned_data)


class AnswerForm(forms.Form):
    text = forms.CharField(max_length=5000, widget=forms.Textarea)
    question = forms.ModelChoiceField(queryset=Question.objects.all(), widget=forms.HiddenInput)

    def __init__(self, user, *args, **kwargs):
        self._user = user
        super().__init__(*args, **kwargs)

    def save(self):
        self.cleaned_data['author'] = self._user
        return Answer.objects.create(**self.cleaned_data)


class SignUpForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=30)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(min_length=4, max_length=30, widget=forms.PasswordInput)

    def clean_username(self):
        user_name = self.cleaned_data.get('username')
        if User.objects.filter(username=user_name).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует')
        return user_name

    def clean_email(self):
        e_mail = self.cleaned_data.get('email')
        if User.objects.filter(email=e_mail).exists():
            raise forms.ValidationError('Пользователь с таким адресом электронной почты уже существует')
        return e_mail

    def save(self):
        user_name = self.cleaned_data.get('username')
        pass_word = self.cleaned_data.get('password')
        e_mail = self.cleaned_data.get('email')
        _ = User.objects.create_user(username=user_name, password=pass_word, email=e_mail)
        auth_user = authenticate(username=user_name, password=pass_word)
        return auth_user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)

    def clean(self):
        user = authenticate(**self.cleaned_data)
        if user is None:
            raise forms.ValidationError('Пожалуйста введите правильные имя пользователя и пароль')
        if not user.is_active:
            raise forms.ValidationError('Ошибка! Пользователь был удален')

    def save(self):
        user_name = self.cleaned_data.get('username')
        pass_word = self.cleaned_data.get('password')
        user = authenticate(username=user_name, password=pass_word)
        return user

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render

from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.http import require_GET

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .models import Question
from .forms import AskForm, AnswerForm, SignUpForm, LoginForm


@require_GET
def index(request):
    questions = Question.objects.new()
    paginator, page = paginate(request, questions)
    paginator.baseurl = '/?page='
    return render(request, 'index.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
        'auth': auth_output(request.user)
    })


@require_GET
def popular(request):
    questions = Question.objects.popular()
    paginator, page = paginate(request, questions)
    paginator.baseurl = '/popular/?page='
    return render(request, 'popular.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
        'auth': auth_output(request.user)
    })


def paginate(req, qs):
    limit = 10
    try:
        page_numb = int(req.GET.get('page', 1))
    except ValueError:
        raise Http404
    if page_numb <= 0:
        page_numb = 1
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page_numb)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return paginator, page


def one_question(request, question_id):
    this_question = get_object_or_404(Question, id=question_id)
    user = request.user
    if user.is_authenticated():
        if request.method == 'POST':
            form = AnswerForm(user, request.POST)
            if form.is_valid():
                _ = form.save()
                new_url = this_question.get_url()
                return HttpResponseRedirect(new_url)
        else:
            form = AnswerForm(user, initial={
                'question': this_question
            })
        return render(request, 'one_question.html', {
            'question': this_question,
            'answers': this_question.answer_set.all()[:],
            'form': form,
            'auth': auth_output(user),
            'is_auth': True
        })
    else:
        return render(request, 'one_question.html', {
            'question': this_question,
            'answers': this_question.answer_set.all()[:],
            'auth': auth_output(user),
            'is_auth': False
        })


@login_required()
def ask(request):
    user = request.user
    if request.method == 'POST':
        form = AskForm(user, request.POST)
        if form.is_valid():
            new_question = form.save()
            new_url = new_question.get_url()
            return HttpResponseRedirect(new_url)
    else:
        form = AskForm(user)
    return render(request, 'ask.html', {
        'form': form,
        'auth': auth_output(user)
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {
        'form': form,
        'auth': auth_output(request.user)
    })


def my_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            new_url = '/'
            return HttpResponseRedirect(new_url)
    else:
        form = LoginForm()
    return render(request, 'login.html', {
        'form': form,
        'auth': auth_output(request.user)
    })


def my_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def auth_output(user):
    if user.is_authenticated:
        return "Вы авторизованы как " + user.get_username()
    else:
        return "Вы не авторизованы"

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render

from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.http import require_GET

from .models import Question, Answer
from .forms import AskForm, AnswerForm


@require_GET
def index(request):
    questions = Question.objects.new()
    paginator, page = paginate(request, questions)
    paginator.baseurl = '/?page='
    return render(request, 'new.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page,
        'title': 'New questions'
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
        'title': 'Popular questions'
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
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            new_answer = form.save()
            new_url = this_question.get_url()
            return HttpResponseRedirect(new_url)
    else:
        form = AnswerForm(initial={'question': this_question})
    return render(request, 'one_question.html', {
        'question': this_question,
        'answers': this_question.answer_set.all()[:],
        'form': form
    })


def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            new_question = form.save()
            new_url = new_question.get_url()
            return HttpResponseRedirect(new_url)
    else:
        form = AskForm()
    return render(request, 'question_add.html', {
        'form': form
    })


@require_GET
def test(request, *args, **kwargs):
    return HttpResponse('OK')

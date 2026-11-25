from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from questions.forms import QuestionForm, AnswerForm
from questions.models import Question, Answer, Tag

from django.shortcuts import render, get_object_or_404, redirect


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
        return page_obj
    except (PageNotAnInteger, EmptyPage):
        page_number = 1
        page_obj = paginator.page(page_number)
        return page_obj


def index(request):
    page_obj = paginate(Question.objects.new(), request)
    return render(request, 'questions/index.html', context={'Questions': page_obj.object_list, 'page_obj': page_obj})

def hot(request):
    page_obj = paginate(Question.objects.best(), request)
    return render(request, 'questions/hot.html', context={'Questions': page_obj.object_list, 'page_obj': page_obj})

@login_required(login_url='login')
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(request.user)
            return redirect(question.get_absolute_url())
    else:
        form = QuestionForm()
    return render(request, 'questions/ask.html', context={'form': form})


def search(request):
    query = request.GET.get('query', '')
    page_obj = paginate(Question.objects.search(query), request)
    return render(request, 'questions/index.html', context={'Questions': page_obj.object_list, 'page_obj': page_obj, 'query': query})

def tags(request, tag_name):
    get_object_or_404(Tag, name_tag=tag_name)
    page_obj = paginate(Question.objects.by_tag(tag_name), request)
    return render(request, 'questions/tags.html', context={'Questions': page_obj.object_list, 'page_obj': page_obj, 'tag': tag_name})

def question(request, question_id):
    question_cur = get_object_or_404(Question.objects.new(), pk=question_id)
    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(request.user, question_cur)
            page = Answer.objects.page_of(answer)
            return redirect(f"{question_cur.get_absolute_url()}?page={page}#answer-{answer.id}")
    else:
        form = AnswerForm()
    page_obj = paginate(Answer.objects.for_question(question_id), request)
    return render(request, 'questions/question.html', context={'question': question_cur, 'Questions': page_obj.object_list, 'page_obj': page_obj, 'form': form})



@require_POST
@login_required
def like_question(request, question_id, vote_type):
    quest = get_object_or_404(Question, pk=question_id)
    return JsonResponse({'count': quest.vote(request.user, vote_type == 'like')})


@require_POST
@login_required
def like_answer(request, answer_id, vote_type):
    answer = get_object_or_404(Answer, pk=answer_id)
    return JsonResponse({'count': answer.vote(request.user, vote_type == 'like')})

@require_POST
@login_required
def best_answer(request, question_id, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id, question_id=question_id)
    if not answer.answer_best(request.user):
        return JsonResponse({'error': 'forbidden'}, status=403)
    return JsonResponse({'ok': True})
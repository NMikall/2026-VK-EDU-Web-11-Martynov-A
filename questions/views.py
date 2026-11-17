from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from questions.models import Question, Answer, Tag

from django.shortcuts import render, get_object_or_404


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
        return page_obj
    except PageNotAnInteger:
        page_number = 1
        page_obj = paginator.page(page_number)
        return page_obj
    except EmptyPage:
        page_number = paginator.num_pages
        page_obj = paginator.page(page_number)
        return page_obj


def index(request):
    page_obj = paginate(Question.objects.new(), request)
    return render(request, 'questions/index.html', context={'Questions': page_obj.object_list, 'page_obj': page_obj})

def hot(request):
    page_obj = paginate(Question.objects.best(), request)
    return render(request, 'questions/hot.html', context={'Questions': page_obj.object_list, 'page_obj': page_obj})

def ask(request):
    return render(request, 'questions/ask.html')

def tags(request, tag_name):
    get_object_or_404(Tag, name_tag=tag_name)
    page_obj = paginate(Question.objects.by_tag(tag_name), request)
    return render(request, 'questions/tags.html', context={'Questions': page_obj.object_list, 'page_obj': page_obj, 'tag': tag_name})

def question(request, question_id):
    question_cur = get_object_or_404(Question.objects.new(), pk=question_id)
    page_obj = paginate(Answer.objects.for_question(question_id), request)
    return render(request, 'questions/question.html', context={'question': question_cur, 'Questions': page_obj.object_list, 'page_obj': page_obj})
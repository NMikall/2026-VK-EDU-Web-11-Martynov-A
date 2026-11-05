from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.

QUESTION_LIST = [
    {
        'title': f'Title {i}',
        'text': f'Text {i}' * 10,
        'id': i,
    } for i in range(90)
]

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
    page_obj = paginate(QUESTION_LIST, request)
    return render(request, 'questions/index.html', context={'Questions': page_obj.object_list, 'page_obj': page_obj})

def hot(request):
    page_obj = paginate(QUESTION_LIST[::-1], request)
    return render(request, 'questions/hot.html', context={'Questions': page_obj.object_list, 'page_obj': page_obj})

def ask(request):
    return render(request, 'questions/ask.html', context={'Questions': QUESTION_LIST[::-1]})

def tags(request, tag_name):
    page_obj = paginate(QUESTION_LIST, request)
    return render(request, 'questions/tags.html', context={'Questions': page_obj.object_list, 'page_obj': page_obj, 'tag': tag_name})

def question(request, question_id):
    page_obj = paginate(QUESTION_LIST, request)
    return render(request, 'questions/question.html', context={'Questions': page_obj.object_list, 'page_obj': page_obj})
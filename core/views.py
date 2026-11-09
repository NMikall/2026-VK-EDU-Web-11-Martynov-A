from django.core.paginator import Paginator
from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.

QUESTION_LIST = [
    {
        'title': f'Title {i}',
        'text': f'Text {i}' * 10,
    } for i in range(30)
]


def profile(request):
    return render(request, 'core/profile.html', context={'Questions': QUESTION_LIST[::-1]})

def login(request):
    return render(request, 'core/login.html', context={'Questions': QUESTION_LIST[::-1]})

def signup(request):
    return render(request, 'core/signup.html', context={'Questions': QUESTION_LIST[::-1]})

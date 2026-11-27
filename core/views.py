from django.contrib import auth
from django.http.response import HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme

from django.urls import reverse

from core.forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from core.forms import UserUpdateForm, ProfileUpdateForm
from core.models import Profile


# Create your views here.


@login_required(login_url='login')
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile_obj)
    return render(request, 'core/profile.html', context={'user_form': user_form, 'profile_form': profile_form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.user)
            url = request.GET.get('next', None)
            if url is None or url == "" or not url_has_allowed_host_and_scheme(url, allowed_hosts={request.get_host()}):
                return redirect('index')
            return redirect(url)
    else:
        form = LoginForm()
    return render(request, 'core/login.html', context={'form': form})

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegistrationForm()
    return render(request, 'core/signup.html', context={'form': form})

def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'index'))
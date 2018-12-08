from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect

from services.forms.accounts import LoginForm, SignUpForm, ProfileForm


def signup(request: HttpRequest) -> redirect or render:
    if request.method == 'GET':
        return render(request, 'account/signup.html', context={
            'form': SignUpForm()
        })
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        # login
        user = authenticate(username=form.cleaned_data['email'],
                            password=form.cleaned_data['password1'])
        login(request, user)
        return redirect('/')
    return render(request, 'account/signup.html', context={
        'form': form
    })


def login_view(request: HttpRequest) -> redirect or render:
    if request.method == 'GET':
        return render(request, 'account/login.html', context={
            'form': LoginForm()
        })
    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            return redirect('/')
    return render(request, 'account/login.html', context={
        'form': form
    })


@login_required
def logout_view(request: HttpRequest) -> redirect:
    logout(request)
    return redirect('/')

from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.shortcuts import render, redirect

from services.forms.accounts import SignUpForm


def signup(request: HttpRequest) -> render:
    if request.method == 'GET':
        return render(request, 'signup.html', context={
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
    return render(request, 'signup.html', context={
        'form': form
    })

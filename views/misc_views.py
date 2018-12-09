from django.shortcuts import render, redirect
from django.http import HttpRequest

from infrastructure.models import Ward
from services.forms.contacts import ContactForm
from services.zendesk import create_ticket


def about(request: HttpRequest) -> render:
    return render(request, 'misc/about.html', context={
        'wards': Ward.objects.filter(is_active=True)
    })


def contact(request: HttpRequest) -> render:
    if request.method == 'GET':
        return render(request, 'misc/contact.html', {
            'form': ContactForm()
        })
    form = ContactForm(request.POST)
    if form.is_valid():
        create_ticket(
            username=form.cleaned_data['fullname'],
            email=form.cleaned_data['email'],
            title=form.cleaned_data['title'],
            description=form.cleaned_data['description']
        )
        messages = 'お問い合わせを完了しました'
        return render(request, 'misc/contact.html', {
            'form': ContactForm(),
            'messages': messages
        })
    return render(request, 'misc/contact.html', {
        'form': form
    })

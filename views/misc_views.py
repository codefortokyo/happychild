from django.shortcuts import render
from django.http import HttpRequest

from infrastructure.mysql import Ward


def about(request: HttpRequest) -> render:
    return render(request, 'about.html', context={
        'wards': Ward.objects.filter(is_active=True)
    })


def contact(request: HttpRequest) -> render:
    return render(request, 'contact.html')

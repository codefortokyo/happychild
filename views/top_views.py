from django.shortcuts import render
from django.http import HttpRequest


def index(request: HttpRequest) -> render:
    return render(request, 'index.html')

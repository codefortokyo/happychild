from django.shortcuts import render
from django.http import HttpRequest

from services.forms.searches import SearchLocationForm, SearchTypeForm, SearchFeatureForm


def index(request: HttpRequest) -> render:
    return render(request, 'index.html', context={
        'location_form': SearchLocationForm(),
        'type_form': SearchTypeForm(),
        'feature_form': SearchFeatureForm()
    })

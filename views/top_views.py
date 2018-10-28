from django.shortcuts import render
from django.http import HttpRequest

from infrastructure.models import Ward
from services.forms.searches import SearchLocationForm, SearchTypeForm, SearchFeatureForm

DEFAULT_WARD_ID = 9


def index(request: HttpRequest) -> render:
    ward = Ward.objects.filter(id=DEFAULT_WARD_ID).first()
    return render(request, 'index.html', context={
        'location_form': SearchLocationForm(initial={
            'city': ward.city_id,
            'ward': ward.id
        }, city_id=ward.city_id, ward_id=ward.id),
        'type_form': SearchTypeForm(),
        'feature_form': SearchFeatureForm(),
    })


import json
from django.shortcuts import render
from django.http import HttpRequest

from infrastructure.models import Ward
from services.forms.searches import SearchLocationForm, SearchTypeForm, SearchFeatureForm
from services.transformers import transform_forms_to_search_nursery
from infrastructure.entities.searches import SearchNurseryEntity
from services.searches import get_nurseries

DEFAULT_WARD_ID = 9


def search_nurseries(request: HttpRequest) -> render:
    city_id = request.GET.get('city')
    ward_id = request.GET.get('ward')
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    score = request.GET.get('score')
    hierarchy = request.GET.get('hierarchy')

    location_form = SearchLocationForm(city_id, ward_id, latitude, longitude, data=request.GET)
    type_form = SearchTypeForm(data=request.GET)
    feature_form = SearchFeatureForm(data=request.GET)

    if location_form.is_valid() and type_form.is_valid() and feature_form.is_valid():
        parameters = transform_forms_to_search_nursery(location_form, type_form, feature_form, score, hierarchy)
    else:
        ward = Ward.objects.filter(id=DEFAULT_WARD_ID).first()
        parameters = SearchNurseryEntity(city_id=ward.city_id, ward_id=ward.id)
        location_form = SearchLocationForm(initial={
            'city': ward.city_id,
            'ward': ward.id
        }, city_id=ward.city_id, ward_id=ward.id)

    nurseries, geo_parameters = get_nurseries(parameters)

    return render(request, 'search/nursery.html', context={
        'location_form': location_form,
        'type_form': type_form,
        'feature_form': feature_form,
        'latitude': geo_parameters.origin_coordinate.get('latitude'),
        'longitude': geo_parameters.origin_coordinate.get('longitude'),
        'nurseries': json.dumps({'data': nurseries})
    })

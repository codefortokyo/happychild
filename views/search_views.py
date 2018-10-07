import json
from django.shortcuts import render
from django.http import HttpRequest

from infrastructure.mysql import Ward
from services.forms import SearchLocationForm, SearchTypeForm, SearchFeatureForm
from services.transformers import transform_forms_to_search_nursery
from services.entities import SearchNurseryEntity
from services.searches import get_nurseries

DEFAULT_WARD_ID = 24


def search_nurseries(request: HttpRequest) -> render:
    city_id = request.GET.get('city')
    ward_id = request.GET.get('ward')
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    location_form = SearchLocationForm(city_id, ward_id, latitude, longitude, data=request.GET)
    type_form = SearchTypeForm(data=request.GET)
    feature_form = SearchFeatureForm(data=request.GET)

    if location_form.is_valid() and type_form.is_valid() and feature_form.is_valid():
        parameters = transform_forms_to_search_nursery(location_form, type_form, feature_form)
    else:
        ward = Ward.objects.filter(id=DEFAULT_WARD_ID).first()
        parameters = SearchNurseryEntity(city_id=ward.city_id, ward_id=ward.id)
        location_form = SearchLocationForm(initial={
            'city': ward.city_id,
            'ward': ward.id
        }, city_id=ward.city_id, ward_id=ward.id)

    nurseries, geo_parameters = get_nurseries(parameters)

    return render(request, 'search.html', context={
        'location_form': location_form,
        'type_form': type_form,
        'feature_form': feature_form,
        'latitude': geo_parameters.origin_coordinate.get('latitude'),
        'longitude': geo_parameters.origin_coordinate.get('longitude'),
        'nurseries': json.dumps({'data': nurseries})
    })

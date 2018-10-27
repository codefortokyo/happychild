import json

from django.http import HttpRequest, HttpResponse

from infrastructure.repository.query import get_nearest_ward, get_near_stations
from infrastructure.models import Ward, Station


# TODO: validate
def get_wards(request: HttpRequest) -> HttpResponse:
    return HttpResponse(Ward.get_wards(int(request.GET.get('city_id'))), content_type='application/json')


def get_stations(request: HttpRequest) -> HttpResponse:
    return HttpResponse(Station.get_stations_api(int(request.GET.get('ward_id'))), content_type='application/json')


def get_near_ward_and_stations(request: HttpRequest) -> HttpResponse:
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    ward_id = get_nearest_ward(latitude, longitude)
    city_id = Ward.objects.filter(id=ward_id).first().city_id

    wards = Ward.objects.filter(city_id=city_id)
    stations = get_near_stations(latitude, longitude)
    ret = json.dumps({
        'selected_city_id': city_id,
        'selected_ward_id': ward_id,
        'wards': [{'id': ward.id, 'name': ward.name} for ward in wards],
        'stations': [{'id': station['id'], 'name': station['name']} for station in stations]
    })
    return HttpResponse(ret, content_type='application/json')

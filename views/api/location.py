from django.http import HttpRequest, HttpResponse

from infrastructure.mysql import Ward, Station

# TODO: validate


def get_wards(request: HttpRequest) -> HttpResponse:
    return HttpResponse(Ward.get_wards(int(request.GET.get('city_id'))), content_type='application/json')


def get_stations(request: HttpRequest) -> HttpResponse:
    return HttpResponse(Station.get_stations_api(int(request.GET.get('ward_id'))), content_type='application/json')

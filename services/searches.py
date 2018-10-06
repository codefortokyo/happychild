import json
from decimal import Decimal
from typing import Dict, List, Tuple

from infrastructure.mysql import Nursery, Station, Ward
from infrastructure.query import get_nearest_ward, get_near_nurseries
from services.entities import GeoParameterEntity, SearchNurseryEntity, NurseryEntity


def get_nurseries(search: SearchNurseryEntity, limit: int = 50) -> Tuple[List[dict], GeoParameterEntity]:
    geo_parameters = _get_geo_parameters(search)
    nurseries = _get_nurseries(search)

    return [json.loads(NurseryEntity(
        id=n.id,
        license=n.license.name,
        school_type=n.license.name,
        name=n.name,
        postcode=n.postcode,
        address=n.address,
        station_info=n.station_info,
        url=n.url,
        image=n.default_thumbnail_url,
        latitude=float(n.latitude),
        longitude=float(n.longitude),  # Object of type Decimal is not JSON serializable
        open_time_weekday=n.default_open_time_weekday,
        open_time_saturday=n.default_open_time_saturday,
        accept_age=n.accept_age,
        stable_food=n.stable_food,
        temporary_childcare=n.temporary_childcare,
        overnight_childcare=n.overnight_childcare,
        allday_childcare=n.allday_childcare,
        evaluation=n.evaluation,
        organizer=n.organizer,
        event=n.default_event,
        service=n.default_service,
        policy=n.default_policy,
        promise=n.promise,
        free_num_not_one=n.free_nums.free_num_not_one,
        free_num_one_year_old=n.free_nums.free_num_one_year_old,
        free_num_two_year_old=n.free_nums.free_num_two_year_old,
        free_num_three_year_old=n.free_nums.free_num_three_year_old,
        free_num_four_year_old=n.free_nums.free_num_four_year_old,
        free_num_extent=n.free_nums.free_num_extent,
        free_num_updated_at=str(n.free_nums.latest_modified_date)
    ).to_json()) for n in nurseries[:limit]], geo_parameters


def _get_nurseries(search: SearchNurseryEntity) -> List[Nursery]:
    """
    Get filtered nursery data from db

    Parameters
    ----------
    search ``SearchNurseryEntity``, required
        query parameters

    Returns
    -------
    Query result of searching nurseries
    """
    if search.latitude and search.longitude:
        nursery_ids = list(n['id'] for n in get_near_nurseries(latitude=search.latitude, longitude=search.longitude))
        nurseries = Nursery.objects.select_related('license', 'school_type').filter(id__in=nursery_ids, is_active=True)
    else:
        nurseries = Nursery.objects.select_related('license', 'school_type').filter(ward_id=search.ward_id,
                                                                                    is_active=True)
    # filtering by nursery types
    if search.license_id:
        nurseries = nurseries.filter(license_id=search.license_id)
    if search.school_type_id:
        nurseries = nurseries.filter(school_type_id=search.school_type_id)

    # filtering by nursery features
    if search.stable_food:
        nurseries = nurseries.filter(stable_food=True)
    if search.temporary_childcare:
        nurseries = nurseries.filter(temporary_childcare=True)
    if search.overnight_childcare:
        nurseries = nurseries.filter(overnight_childcare=True)
    if search.allday_childcare:
        nurseries = nurseries.filter(allday_childcare=True)
    if search.evaluation:
        nurseries = nurseries.filter(evaluation=True)

    if search.is_opening:
        if search.age_id:
            nurseries = [nursery for nursery in nurseries if nursery.free_nums.is_opening_by_age(search.age_id)]
        else:
            nurseries = [nursery for nursery in nurseries if nursery.free_nums.is_opening()]
    return nurseries


def _get_geo_parameters(search: SearchNurseryEntity) -> GeoParameterEntity:
    """
    Get parameters related Geo coordinates

    Parameters
    ----------
    search ``SearchNursery``, required

    Returns
    -------
    Geo parameters
    """
    if search.latitude and search.longitude and search.station_id:
        station = Station.objects.filter(id=search.station_id).first()
        return GeoParameterEntity(
            ward_id=get_nearest_ward(search.latitude, search.longitude),
            origin_coordinate=_geo_dictionary(search.latitude, search.longitude),
            destination_coordinate=_geo_dictionary(station.latitude, station.longitude))

    if search.station_id:
        station = Station.objects.filter(id=search.station_id).first()
        return GeoParameterEntity(
            ward_id=get_nearest_ward(station.latitude, station.longitude),
            origin_coordinate=_geo_dictionary(station.latitude, station.longitude),
            destination_coordinate=_geo_dictionary(station.latitude, station.longitude))

    if search.latitude and search.longitude:
        return GeoParameterEntity(
            ward_id=get_nearest_ward(search.latitude, search.longitude),
            origin_coordinate=_geo_dictionary(search.latitude, search.longitude),
            destination_coordinate=_geo_dictionary(search.latitude, search.longitude))

    ward = Ward.objects.filter(id=search.ward_id).first()
    return GeoParameterEntity(
        ward_id=search.ward_id,
        origin_coordinate=_geo_dictionary(ward.latitude, ward.longitude),
        destination_coordinate=_geo_dictionary(ward.latitude, ward.longitude))


def _geo_dictionary(latitude: Decimal, longitude: Decimal) -> Dict[Decimal, Decimal]:
    """
    Convert coordinate values to dict
    Parameters
    ----------
    latitude ``decimal``, required
    longitude ``decimal``, required

    Returns
    -------
    Dict of coordinates
    """
    d = dict()
    d['latitude'] = latitude
    d['longitude'] = longitude
    return d

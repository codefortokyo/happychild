import json
from decimal import Decimal
from typing import Dict, List, Tuple

from infrastructure.models import Nursery, NurseryFreeNum, NurseryScore, Station, Ward
from infrastructure.consts import (
    NURSERY_FREE_NUM_FMT,
    NOT_ONE_AGE_ID,
    ONE_YEAR_OLD_AGE_ID,
    TWO_YEAR_OLD_AGE_ID,
    THREE_YEAR_OLD_AGE_ID,
    FOUR_YEAR_OLD_AGE_ID,
    EXTENT_AGE_ID,
    AGE_IDS,
)
from infrastructure.repository.query import get_nearest_ward, get_near_nurseries
from infrastructure.entities.nurseries import NurseryEntity
from infrastructure.entities.searches import GeoParameterEntity, SearchNurseryEntity


def get_nurseries(search: SearchNurseryEntity, limit: int = 50) -> Tuple[List[str], GeoParameterEntity]:
    geo_parameters = _get_geo_parameters(search)
    nurseries = _get_nurseries(search)

    nursery_ids = [n.id for n in nurseries]
    free_nums = NurseryFreeNum.get_free_nums(nursery_ids)
    last_updated_dates = NurseryFreeNum.get_last_updated_date(nursery_ids)

    nurseries = _filter_by_free_nums(nurseries, search, free_nums)
    nurseries = _filter_by_scores(nurseries, search)

    nurseries = sorted(nurseries, key=lambda x: x.updated_at, reverse=True)

    return [json.loads(NurseryEntity(
        id=n.id,
        license=n.license.name,
        school_type=n.school_type.name,
        name=n.name,
        postcode=n.postcode,
        address=n.address,
        station_info=n.station_info,
        url=n.url,
        image=n.thumbnail_url,
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
        free_num_not_one=free_nums.get(NURSERY_FREE_NUM_FMT.format(n.id, NOT_ONE_AGE_ID), 0),
        free_num_one_year_old=free_nums.get(NURSERY_FREE_NUM_FMT.format(n.id, ONE_YEAR_OLD_AGE_ID), 0),
        free_num_two_year_old=free_nums.get(NURSERY_FREE_NUM_FMT.format(n.id, TWO_YEAR_OLD_AGE_ID), 0),
        free_num_three_year_old=free_nums.get(NURSERY_FREE_NUM_FMT.format(n.id, THREE_YEAR_OLD_AGE_ID), 0),
        free_num_four_year_old=free_nums.get(NURSERY_FREE_NUM_FMT.format(n.id, FOUR_YEAR_OLD_AGE_ID), 0),
        free_num_extent=free_nums.get(NURSERY_FREE_NUM_FMT.format(n.id, EXTENT_AGE_ID), 0),
        free_num_updated_at=str(last_updated_dates.get(n.id, '-'))
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
    nurseries = _filter_by_nursery_location_and_type(nurseries, search)
    return nurseries


def _filter_by_nursery_location_and_type(nurseries: Nursery.objects, search: SearchNurseryEntity) -> Nursery.objects:
    """
    Filtering nurseries by location and types

    Parameters
    ----------
    nurseries ``Nursery.objects``, required
    search ``SearchNurseryEntity``, required

    Returns
    -------
    Result of query filtering
    """
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
    return nurseries


def _filter_by_free_nums(nurseries: List[Nursery], search: SearchNurseryEntity, free_nums: dict) -> List[Nursery]:
    """
    Filtering nurseries by free nums(spaces)

    Parameters
    ----------
    nurseries ``Nursery.objects``, required
    search ``SearchNurseryEntity``, required
    free_nums ``dict``, required
        dict of free nums, key: NURSERY_FREE_NUM_FMT(nursery_id, age_id) str, value: free_num int

    Returns
    -------
    Result of filtering by free nums
    """
    if not search.is_opening:
        return nurseries

    if search.age_id:
        return [nursery for nursery in nurseries if
                free_nums.get(NURSERY_FREE_NUM_FMT.format(nursery.id, search.age_id), 0) > 0]
    ret = []
    for nursery in nurseries:
        sum_free_num = sum([free_nums.get(NURSERY_FREE_NUM_FMT.format(nursery.id, age_id), 0) for age_id in AGE_IDS])
        if sum_free_num > 0:
            ret.append(nursery)
    return ret


def _filter_by_scores(nurseries: List[Nursery], search: SearchNurseryEntity) -> List[Nursery]:
    """
    Filtering nurseries by score and hierarchy
    TODO: filter by hierarchy

    Parameters
    ---------
    nurseries ``Nursery.objects``, required
    search ``SearchNurseryEntity``, required

    Returns
    -------
    Result of filtering by score and hierarchy
    """
    if not search.score or not search.hierarchy:
        return nurseries

    ret = []
    for nursery in nurseries:
        if not search.score:
            ret.append(nursery)
            continue

        nursery_score = NurseryScore.get_last_year_score(nursery.id, search.age_id)
        if not nursery_score or not nursery_score.score:
            continue

        if nursery_score.score >= search.score:
            ret.append(nursery)
            continue
    return ret


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

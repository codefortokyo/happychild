import datetime
from decimal import Decimal
from dataclasses import dataclass
from typing import Dict, Optional

from dataclasses_json import dataclass_json

from infrastructure.models import Nursery, Age


@dataclass
class SearchNurseryEntity:
    city_id: int
    ward_id: int
    station_id: Optional[int] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    age_id: Optional[int] = None
    license_id: Optional[int] = None
    school_type_id: Optional[int] = None
    is_opening: Optional[bool] = False
    stable_food: Optional[bool] = False
    temporary_childcare: Optional[bool] = False
    overnight_childcare: Optional[bool] = False
    allday_childcare: Optional[bool] = False
    evaluation: Optional[bool] = False


@dataclass
class GeoParameterEntity:
    ward_id: int
    origin_coordinate: Optional[Dict[Decimal, Decimal]]
    destination_coordinate: Optional[Dict[Decimal, Decimal]]


@dataclass
class NurseryFreeNumEntity:
    nursery: Nursery
    age: Age
    free_num: int
    modified_date: datetime.datetime.date


@dataclass_json
@dataclass
class NurseryEntity:
    id: int
    license: str
    school_type: str
    name: str
    postcode: str
    address: str
    station_info: str
    url: str
    image: str
    latitude: float
    longitude: float
    open_time_weekday: str
    open_time_saturday: str
    accept_age: str
    stable_food: bool
    temporary_childcare: bool
    overnight_childcare: bool
    allday_childcare: bool
    evaluation: bool
    organizer: str
    event: str
    service: str
    policy: str
    promise: str
    free_num_not_one: int or str
    free_num_one_year_old: int or str
    free_num_two_year_old: int or str
    free_num_three_year_old: int or str
    free_num_four_year_old: int or str
    free_num_extent: int or str
    free_num_updated_at: str or str

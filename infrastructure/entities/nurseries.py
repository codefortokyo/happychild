import datetime
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from infrastructure.models import Nursery, Age


@dataclass
class NurseryFreeNumEntity:
    nursery: Nursery
    age: Age
    free_num: int
    modified_date: datetime.datetime.date


@dataclass
class NurseryScoreEntity:
    nursery: Nursery
    age: Age
    year: str
    score: int
    hierarchy: str


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

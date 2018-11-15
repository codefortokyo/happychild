from decimal import Decimal
from dataclasses import dataclass
from typing import Dict, Optional


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
    score: Optional[int] = None
    hierarchy: Optional[str] = None


@dataclass
class GeoParameterEntity:
    ward_id: int
    origin_coordinate: Optional[Dict[Decimal, Decimal]]
    destination_coordinate: Optional[Dict[Decimal, Decimal]]

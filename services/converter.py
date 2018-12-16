from typing import Tuple

import requests
from bs4 import BeautifulSoup

GEOCODING_API_URL = 'http://www.geocoding.jp/api/'


def convert_address_to_geocode(address) -> Tuple[float, float]:
    payload = {'q': address}
    response = requests.get(GEOCODING_API_URL, params=payload)
    ret = BeautifulSoup(response.content, 'lxml')
    if ret.find('error'):
        raise ValueError(f"Invalid address submitted. {address}")
    else:
        lat = float(ret.find('lat').string)
        lon = float(ret.find('lng').string)
    return lat, lon

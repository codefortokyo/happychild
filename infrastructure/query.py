import decimal
from typing import Dict, List

from django.db import connections
from django.utils.lru_cache import lru_cache


def dictfetchall(cursor: connections) -> List[Dict]:
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def get_near_nurseries(latitude: decimal, longitude: decimal, distance: int = 10, limit: int = 50) -> List[Dict]:
    """ 指定された地点に近い保育園情報を取得する
    """
    cursor = connections['replica'].cursor()
    cursor.execute("""
        SELECT
          id,
          name,
            ST_Distance_Sphere(POINT(longitude, latitude), POINT({longitude}, {latitude}))/1000 as distance
        FROM
          nurseries
        WHERE
          latitude IS NOT NULL
          AND longitude IS NOT NULL
        ORDER BY
          distance
        LIMIT {limit}
        """.format(latitude=latitude, longitude=longitude, distance=distance, limit=limit))
    return list(dictfetchall(cursor))


@lru_cache(maxsize=100)
def get_near_stations(latitude: decimal, longitude: decimal, distance: int = 10, limit: int = 30) -> List[Dict]:
    """ 指定された地点に近い駅情報を取得する
    """
    cursor = connections['replica'].cursor()
    cursor.execute("""
        SELECT
          MIN(id) as id,
          name,
            MIN(ST_Distance_Sphere(POINT(longitude, latitude), POINT({longitude}, {latitude}))/1000) as distance
        FROM
          stations
        WHERE
          latitude IS NOT NULL
          AND longitude IS NOT NULL
        GROUP BY
          name
        ORDER BY
          distance
        """.format(latitude=latitude, longitude=longitude, distance=distance, limit=limit))
    return list(dictfetchall(cursor))


@lru_cache(maxsize=100)
def get_nearest_ward(latitude: decimal, longitude: decimal) -> int:
    """ 最も近い地区を返す
    """
    cursor = connections['replica'].cursor()
    cursor.execute("""
      SELECT
        *,
        ST_Distance_Sphere(POINT(longitude, latitude), POINT({longitude}, {latitude}))/1000 as distance
      FROM
        wards
      ORDER BY
        distance
      LIMIT 1
      """.format(latitude=latitude, longitude=longitude))
    return list(dictfetchall(cursor))[0]['id']

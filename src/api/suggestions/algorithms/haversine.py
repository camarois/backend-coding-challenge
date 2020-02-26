from math import radians, sin, cos, asin, sqrt

EARTH_RADIUS_KM = 6371.0
HALF_EARTH_CIRCUMFERENCE_KM = 10010


def _ratio(haversine_distance: float):
    return haversine_distance / HALF_EARTH_CIRCUMFERENCE_KM


def _haversine_distance(latitude1: float, longitude1: float, latitude2: float, longitude2: float):
    longitude1, latitude1, longitude2, latitude2 = map(radians, [longitude1, latitude1, longitude2, latitude2])
    diff_longitude = longitude2 - longitude1
    diff_latitude = latitude2 - latitude1
    temp = sin(diff_latitude / 2) ** 2 + cos(latitude1) * cos(latitude2) * sin(diff_longitude / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(temp))


def calculate_haversine_score(latitude1: float, longitude1: float, latitude2: float, longitude2: float):
    distance = _haversine_distance(latitude1, longitude1, latitude2, longitude2)
    return _ratio(distance)

from src.api.suggestions.algorithms import haversine

TORONTO = (43.70011, -79.4163)
NYC = (40.71427, -74.00597)

def test_haversine_distance():
    expected_distance = 555.5033
    actual_distance = haversine._haversine_distance(TORONTO[0], TORONTO[1], NYC[0], NYC[1])

    assert round(abs(expected_distance - actual_distance), 4) == 0

def test_haversine_ratio():
    expected_distance = 555.5033
    expected_ratio = expected_distance / haversine.HALF_EARTH_CIRCUMFERENCE_KM
    actual_ratio = haversine._ratio(expected_distance)

    assert expected_ratio == actual_ratio

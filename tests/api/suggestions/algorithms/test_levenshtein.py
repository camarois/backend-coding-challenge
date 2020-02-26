# import pytest
# from src.api.suggestions.cityInterface import CityInterface
# from src.api.suggestions.algorithms import levenshtein

# q = "toront"
# city = CityInterface(
#     id="5174095",
#     name="Toronto",
#     alt_names=["Toronto"],
#     country="US",
#     longitude=-80.60091,
#     latitude=40.46423
# )


# # def test_calculate_levenshtein_score(q: str, city: CityInterface):
# #     expected_distance = 555.5041
# #     actual_distance = haversine._haversine_distance(TORONTO[0], TORONTO[1], NYC[0], NYC[1])

# #     assert abs(expected_distance - actual_distance) == 0

# def test_levenshtein_ratio():
#     expected_distance = 555.5041
#     expected_ratio = expected_distance / haversine.HALF_EARTH_CIRCUMFERENCE_KM
#     actual_ratio = haversine._ratio(expected_distance)

#     assert expected_ratio == actual_ratio

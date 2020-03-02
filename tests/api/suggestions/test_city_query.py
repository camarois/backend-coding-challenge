import pytest
from src.api.suggestions.city_query import CityQuery
import src.utils.suffix_tree as sf
from src.utils.format_helper import normalize_input


@pytest.fixture(scope="module")
def client():
    tree = sf.SuffixTree()
    return CityQuery(tree)


def test_get_cities_response_with_valid_parameters(client):
    response = client.get(normalize_input("Toronto"), 43.70011, -79.4163)
    cities = response["suggestions"]
    assert any(city.name == "Toronto, CA" for city in cities)
    assert any(city.latitude == "43.70011" for city in cities)
    assert any(city.longitude == "-79.4163" for city in cities)


def test_get_cities_response_with_empty_query_returns_type_error(client):
    response = client.get(normalize_input(""), 43.70011, -79.4163)
    assert len(response["suggestions"]) == 0


def test_get_cities_response_with_invalid_latitude_returns_type_error(client):
    with pytest.raises(TypeError) as e:
        client.get(normalize_input("Toronto"), "43.70011", -79.4163)
    assert e.type is TypeError


def test_get_cities_response_with_invalid_longitude_returns_type_error(client):
    with pytest.raises(TypeError) as e:
        client.get(normalize_input("Toronto"), 43.70011, "-79.4163")
    assert e.type is TypeError

import http
from urllib.parse import quote_plus, urlencode
import pytest
import src.api.server as server 


ROOT_PATH = "/"
SUGGESTIONS_PATH = "/suggestions"


def get(client, path, data):
    url = path + "?" + urlencode(data, quote_via=quote_plus)
    return client.get(url)


@pytest.fixture
def client():
    app = server.create_app()
    client = app.test_client()
    yield client


def test_get_root_returns_http_temporary_redirect(client):
    response = client.get(ROOT_PATH)
    assert response.status_code == http.HTTPStatus.TEMPORARY_REDIRECT


def test_get_suggestions_with_empty_query_returns_http_ok(client):
    response = client.get(SUGGESTIONS_PATH)
    json_data = response.get_json()
    assert response.status_code == http.HTTPStatus.OK
    assert len(json_data["suggestions"]) == 0


def test_get_suggestions_with_invalid_latitude_returns_http_bad_request(client):
    response = get(client, SUGGESTIONS_PATH, {"latitude": "Not a number"})
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_suggestions_with_invalid_longitude_returns_http_bad_request(client):
    response = get(client, SUGGESTIONS_PATH, {"longitude": "Not a number"})
    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_get_suggestions_with_only_query_returns_http_ok(client):
    response = get(client, SUGGESTIONS_PATH, {"q": "Toronto"})
    json_data = response.get_json()
    suggestions = json_data["suggestions"]

    assert response.status_code == http.HTTPStatus.OK
    assert any(suggestion["name"] == "Toronto, CA" for suggestion in suggestions)
    assert any(suggestion["latitude"] == "43.70011" for suggestion in suggestions)
    assert any(suggestion["longitude"] == "-79.4163" for suggestion in suggestions)


def test_get_suggestions_with_valid_parameters_returns_http_ok(client):
    response = get(client, SUGGESTIONS_PATH, {
        "q": "Toronto",
        "latitude": "43.70011",
        "longitude": "-79.4163"})
    json_data = response.get_json()
    suggestions = json_data["suggestions"]

    assert response.status_code == http.HTTPStatus.OK
    assert any(suggestion["name"] == "Toronto, CA" for suggestion in suggestions)
    assert any(suggestion["latitude"] == "43.70011" for suggestion in suggestions)
    assert any(suggestion["longitude"] == "-79.4163" for suggestion in suggestions)

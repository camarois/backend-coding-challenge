import http
import urllib.parse
import pytest
import src.api.server as server 


ROOT_PATH = "/"
SUGGESTIONS_PATH = "/suggestions"

def get(client, path, data):
    url = path + "?" + urllib.parse.urlencode(data)
    return client.get(url)

@pytest.fixture
def client():
    app = server.create_app()
    client = app.test_client()
    yield client

def test_get_root_returns_HTTP_NOT_FOUND(client):
    response = client.get(ROOT_PATH)
    assert response.status_code == http.HTTPStatus.NOT_FOUND

def test_get_suggestions_with_empty_query_returns_HTTP_OK(client):
    response = client.get(SUGGESTIONS_PATH)
    assert response.status_code == http.HTTPStatus.OK

def test_get_suggestions_with_invalid_latitude_returns_HTTP_BAD_REQUEST(client):
    response = client.get(SUGGESTIONS_PATH, {"latitude":"Not a number"})
    assert response.status_code == http.HTTPStatus.BAD_REQUEST

def test_get_suggestions_with_invalid_longitude_returns_HTTP_BAD_REQUEST(client):
    response = client.get(SUGGESTIONS_PATH, {"longitude":"Not a numbre"})
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
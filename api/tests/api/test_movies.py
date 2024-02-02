from ...app import create_app
import pytest
import requests
from ...app import create_app


@pytest.fixture
def client():
    app = create_app(config_object="api.tests.api.settings")
    with app.test_client() as client:
        yield client


"""START OF RELEASED MOVIES SECTION"""


def test_get_movies_paged(client):
    payload = [[], {"rating": "", "numVotes": ""}]
    response = client.post(
        '/db/movies/pages?page=0&size=3&query=', json=payload)
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert len(response.get_json()["movies"]) == 3


def test_get_movies_by_query(client):
    payload = [[], {"rating": "", "numVotes": ""}]
    response = client.post(
        '/db/movies/pages?page=0&size=3&query=Opp', json=payload)
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert len(response.get_json()["movies"]) == 1


def test_get_movies_by_genres(client):
    payload = [["History"], {"rating": "", "numVotes": ""}]
    response = client.post(
        '/db/movies/pages?page=0&size=3&query=', json=payload)
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert len(response.get_json()["movies"]) == 1


def test_get_movies_by_desc_by_rating(client):
    payload = [[], {"rating": "desc", "numVotes": ""}]
    response = client.post(
        '/db/movies/pages?page=0&size=3&query=', json=payload)
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert response.get_json()["movies"][0]["original_title"] == "Oppenheimer"


def test_get_movies_by_asc_by_rating(client):
    payload = [[], {"rating": "asc", "numVotes": ""}]
    response = client.post(
        '/db/movies/pages?page=0&size=3&query=', json=payload)
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert response.get_json()["movies"][0]["original_title"] == "Aquaman"


def test_get_movies_by_asc_by_num_votes(client):
    payload = [[], {"rating": "", "numVotes": "asc"}]
    response = client.post(
        '/db/movies/pages?page=0&size=3&query=', json=payload)
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert response.get_json()["movies"][0]["original_title"] == "Aquaman"


def test_get_movies_by_desc_by_num_votes(client):
    payload = [[], {"rating": "", "numVotes": "desc"}]
    response = client.post(
        '/db/movies/pages?page=0&size=3&query=', json=payload)
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert response.get_json()["movies"][0]["original_title"] == "Joker"


"""START OF NEW MOVIES SECTION"""


def test_get_new_movies_paged(client):
    payload = [[], {"rating": "", "numVotes": ""}]
    response = client.post(
        '/db/movies/new/pages?page=0&size=3&query=', json=payload)
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert len(response.get_json()["movies"]) == 1


def test_get_new_movies_by_query(client):
    payload = [[], {"rating": "", "numVotes": ""}]
    response = client.post(
        '/db/movies/new/pages?page=0&size=3&query=Bar', json=payload)
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert len(response.get_json()["movies"]) == 1


def test_get_new_movies_by_genres(client):
    payload = [["Comedy"], {"rating": "", "numVotes": ""}]
    response = client.post(
        '/db/movies/new/pages?page=0&size=3&query=', json=payload)
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert len(response.get_json()["movies"]) == 1


def test_get_new_movies_by_desc_by_rating(client):
    payload = [[], {"rating": "desc", "numVotes": ""}]
    response = client.post(
        '/db/movies/new/pages?page=0&size=3&query=', json=payload)
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert response.get_json()["movies"][0]["original_title"] == "Barbie"


def test_get_new_movies_by_asc_by_rating(client):
    payload = [[], {"rating": "asc", "numVotes": ""}]
    response = client.post(
        '/db/movies/new/pages?page=0&size=3&query=', json=payload)
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert response.get_json()["movies"][0]["original_title"] == "Barbie"


def test_get_new_movies_by_asc_by_num_votes(client):
    payload = [[], {"rating": "", "numVotes": "asc"}]
    response = client.post(
        '/db/movies/new/pages?page=0&size=3&query=', json=payload)
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert response.get_json()["movies"][0]["original_title"] == "Barbie"


def test_get_new_movies_by_desc_by_num_votes(client):
    payload = [[], {"rating": "", "numVotes": "desc"}]
    response = client.post(
        '/db/movies/new/pages?page=0&size=3&query=', json=payload)
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert response.get_json()["movies"][0]["original_title"] == "Barbie"

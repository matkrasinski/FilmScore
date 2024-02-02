from ...app import create_app
import pytest
import requests
from ...app import create_app
from ...data.constant.COLUMNS import *


@pytest.fixture
def client():
    app = create_app(config_object="backend.tests.api.settings")
    with app.test_client() as client:
        yield client


def test_all_people(client):
    response = client.get('/db/people')
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert len(response.get_json()) == 20


def test_all_genres(client):
    response = client.get('/db/genres')
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert len(response.get_json()) == 19


def test_all_og_langs(client):
    response = client.get('/db/og_langs')
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_all_collections(client):
    response = client.get('/db/collections')
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert len(response.get_json()) == 6552


def test_all_companies(client):
    response = client.get('/db/companies')
    assert response.content_type == "application/json"
    assert response.status_code == 200
    assert len(response.get_json()) == 177191


def test_movie_details(client):
    response = client.get('/db/movie?id=872585')
    assert response.content_type == "application/json"
    assert response.status_code == 200
    columns = [
        TMDB_ID_COLUMN,
        IMDB_ID_COLUMN,
        ORIGINAL_TITLE_COLUMN,
        GENRES_COLUMN,
        AVERAGE_RATING_TMDB_COLUMN,
        PREDICTED_RATING_COLUMN,
        NUM_VOTES_TMDB_COLUMN,
        KEYWORDS_COLUMN,
        COLLECTION_COLUMN,
        VIDEOS_COLUMN,
        RUNTIME_COLUMN,
        ORIGINAL_LANGUAGE_COLUMN,
        SPOKEN_LANGUAGES_COLUMN,
        STATUS_COLUMN,
        RELEASE_DATE_COLUMN,
        POSTER_SOURCE_COLUMN,
        ACTORS_COLUMN,
        DIRECTORS_COLUMN,
        PRODUCTION_COMPANIES_COLUMN
    ]
    assert set(columns) == set(response.get_json().keys())

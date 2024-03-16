import requests

from ...settings import TMDB_ACCESS_TOKEN, TMDB_API
from ...data.constant.COLUMNS import *


def get_movie_data(id, append_to_response="keywords,videos"):
    url = f'{TMDB_API}movie/{id}?append_to_response={append_to_response}&language=en-US'
    headers = {"accept": "application/json",
               "Authorization": TMDB_ACCESS_TOKEN}
    response = None
    try:
        response = requests.get(url, headers=headers)
        json_body = response.json()
    except:
        print("ERROR OCCURED")
        return {}
    if not json_body.get("success", True):
        return {}
    
    new_data = {
        COLLECTION_COLUMN: json_body.get(COLLECTION_COLUMN, {}).get(ID, "") if json_body.get(COLLECTION_COLUMN) else "",
        BUDGET_COLUMN: json_body.get(BUDGET_COLUMN, 0),
        TMDB_ID_TMDB_COLUMN: id,
        IMDB_ID_COLUMN: json_body.get(IMDB_ID_COLUMN, ""),
        ORIGINAL_LANGUAGE_COLUMN: json_body.get(ORIGINAL_LANGUAGE_COLUMN, ""),
        ORIGINAL_TITLE_COLUMN: json_body.get(ORIGINAL_TITLE_COLUMN, ""),
        STATUS_COLUMN: json_body.get(STATUS_COLUMN, ""),
        RELEASE_DATE_COLUMN: json_body.get(RELEASE_DATE_COLUMN, ""),
        RUNTIME_COLUMN: json_body.get(RUNTIME_COLUMN, 0),
        GENRES_COLUMN: get_names(json_body.get(GENRES_COLUMN, [])),
        PRODUCTION_COMPANIES_COLUMN: get_id(json_body.get(PRODUCTION_COMPANIES_COLUMN, [])),
        SPOKEN_LANGUAGES_COLUMN: get_names(json_body.get(SPOKEN_LANGUAGES_COLUMN, [])),
        KEYWORDS_COLUMN: get_names_nested_field(json_body.get(KEYWORDS_COLUMN, {}), nested_field=KEYWORDS_COLUMN),
        VIDEOS_COLUMN: get_names_nested_field(json_body.get(VIDEOS_COLUMN, {}), nested_field=RESULTS_COLUMN),
    }

    return new_data


def get_names(attribute):
    return "|".join([item[NAME] for item in attribute])


def get_id(attribute):
    return "|".join([str(item[ID]) for item in attribute])


def get_names_nested_field(attribute, nested_field):
    return get_names(attribute.get(nested_field, []))

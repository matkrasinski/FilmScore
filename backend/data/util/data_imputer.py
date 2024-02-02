import pandas as pd
import numpy as np
from ..constant.FILES import TITLE_CREW, TITLE_PRINCIPALS, TITLE_RATINGS, TMDB_COLLECTIONS, TMDB_DATA
from ..constant.COLUMNS import *
from ..constant.NA import NA_ITERABLE, NA_NON_ITERABLE


def prepare_directors(title_crew=TITLE_CREW):
    directors_df = pd.read_csv(title_crew, sep="\t")
    directors_df = directors_df[[TCONST_COLUMN, DIRECTORS_COLUMN]]
    directors_df[DIRECTORS_COLUMN] = directors_df[DIRECTORS_COLUMN].apply(
        lambda x: [] if x == '\\N' else x.split(','))
    return directors_df


def prepare_actors(title_principals=TITLE_PRINCIPALS):
    principals_df = pd.read_csv(title_principals, sep="\t")

    actors_df = principals_df[principals_df[CATEGORY_COLUMN].isin([
                                                                  ACTOR, ACTRESS])]
    actors_df = actors_df.groupby(TCONST_COLUMN)[
        NCONST_COLUMN].agg(list).reset_index()
    actors_df.columns = [TCONST_COLUMN, ACTORS_COLUMN]

    return actors_df


def filter_data(movies, date_criteria="1970-01-01", num_votes_criteria=1000, runtime_criteria=60):
    movies = movies[movies[RUNTIME_COLUMN] != 0]
    movies = movies.drop(
        columns=[BUDGET_COLUMN]) if BUDGET_COLUMN in movies.columns else movies

    movies = movies[movies[RELEASE_DATE_COLUMN] != ""]
    movies = movies[movies[RELEASE_DATE_COLUMN] >= date_criteria]
    movies = movies[movies[NUM_VOTES_IMDB_COLUMN] >= num_votes_criteria]
    movies = movies[movies[RUNTIME_COLUMN] >= runtime_criteria]

    return movies


def adjust_data(data):
    data[GENRES_COLUMN] = data[GENRES_COLUMN].str.split("|")
    data[GENRES_COLUMN] = data[GENRES_COLUMN].apply(
        lambda d: d if isinstance(d, list) else [])

    data[PRODUCTION_COMPANIES_COLUMN] = data[PRODUCTION_COMPANIES_COLUMN].str.split(
        "|")
    data[PRODUCTION_COMPANIES_COLUMN] = data[PRODUCTION_COMPANIES_COLUMN].apply(
        lambda d: d if isinstance(d, list) else [])

    data[SPOKEN_LANGUAGES_COLUMN] = data[SPOKEN_LANGUAGES_COLUMN].str.split(
        "|")
    data[SPOKEN_LANGUAGES_COLUMN] = data[SPOKEN_LANGUAGES_COLUMN].apply(
        lambda d: d if isinstance(d, list) else [])

    data[COLLECTION_COLUMN] = data[COLLECTION_COLUMN].fillna(
        "").apply(lambda x: str(x) if x != "" else "")
    data[KEYWORDS_COLUMN] = data[KEYWORDS_COLUMN].str.replace("|", " ")
    data[VIDEOS_COLUMN] = data[VIDEOS_COLUMN].apply(
        lambda d: d if isinstance(d, str) else '')

    data[ACTORS_COLUMN] = data[ACTORS_COLUMN].apply(
        lambda d: d if isinstance(d, list) else [])
    data[DIRECTORS_COLUMN] = data[DIRECTORS_COLUMN].apply(
        lambda d: d if isinstance(d, list) else [])

    return data


def apply_ratings(data, people_ratings, companies_ratings):
    data[DIRECTORS_RATING_COLUMN] = data[DIRECTORS_COLUMN].apply(lambda x: np.mean(
        [people_ratings[director] for director in x if director in people_ratings]))
    data[ACTORS_RATING_COLUMN] = data[ACTORS_COLUMN].apply(lambda x: np.mean(
        [people_ratings[actor] for actor in x if actor in people_ratings]))
    data[COMPANIES_RATING_COLUMN] = data[PRODUCTION_COMPANIES_COLUMN].apply(lambda x: np.mean(
        [companies_ratings[company] for company in x if company in companies_ratings]))

    print("apply_ratings  ", len(data))
    return data


def fillna_ratings(data):
    data = data.fillna({
        DIRECTORS_RATING_COLUMN: 0.6,
        COMPANIES_RATING_COLUMN: 0.6,
        ACTORS_RATING_COLUMN: 0.6
    })

    return data


def fillna(data):
    def safe_fillna(d, column, value):
        if column in d.columns:
            return d[column].fillna(value, inplace=True)

    def safe_apply(x):
        if isinstance(x, list):
            return x
        elif isinstance(x, str):
            return x.split("|")
        return []

    def safe_fillna_iterable(d, column):
        if column in d.columns:
            d[column] = d[column].apply(lambda x: safe_apply(x))

    for col in NA_ITERABLE:
        safe_fillna_iterable(data, col)
    for col in NA_NON_ITERABLE:
        safe_fillna(data, *col)

    return data


def replace_keywords_sep(data):
    if KEYWORDS_COLUMN in data.columns:
        data[KEYWORDS_COLUMN] = data[KEYWORDS_COLUMN].fillna(
            "").str.replace("|", " ")
    return data

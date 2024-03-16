
import sqlite3

import pandas as pd

from ...extensions import db
from ...database.model import Companies, Movies, MoviesCompanies, MoviesPeople, People
from ...data.util.data_imputer import fillna
from ...data.constant.FILES_NAMES import *
from ...data.constant.COLUMNS import *


def export_movies(path=GENERATED_LOCAL_DIR, save=True):
    conn = sqlite3.connect(DB_LOCAL_PATH)

    movies = pd.read_sql("SELECT * FROM Movies", conn)

    companies = export_movies_companies(save=False)
    companies = companies.groupby(MOVIE_ID_COLUMN)[COMPANY_ID_COLUMN].agg(
        lambda x: '|'.join(map(str, x))).to_dict()

    movies[TMDB_ID_COLUMN] = movies[TMDB_ID_COLUMN].astype(int)
    movies = fillna(movies)
    movies[PRODUCTION_COMPANIES_COLUMN] = movies[TMDB_ID_COLUMN].apply(
        lambda x: companies[x] if x in companies.keys() else "")

    movies[GENRES_COLUMN] = movies[GENRES_COLUMN].apply(lambda x: "|".join(x))
    movies[SPOKEN_LANGUAGES_COLUMN] = movies[SPOKEN_LANGUAGES_COLUMN].apply(
        lambda x: "|".join(x))

    movies.rename(columns={TMDB_ID_COLUMN: TMDB_ID_TMDB_COLUMN}, inplace=True)

    conn.close()

    if save:
        movies.to_csv(f'{path}{EX_MOVIES_NAME}', index=False)

    return movies


def export_movies_people(path=GENERATED_LOCAL_DIR, save=True):
    conn = sqlite3.connect(DB_LOCAL_PATH)

    movies_people = pd.read_sql("SELECT * FROM Movies_People", conn)

    movies_people = fillna(movies_people)

    conn.close()
    if save:
        movies_people.to_csv(f'{path}/{EX_MOVIES_NAME}', index=False)

    return movies_people


def export_movies_companies(path=GENERATED_LOCAL_DIR, save=True):
    conn = sqlite3.connect(DB_LOCAL_PATH)

    movies_companies = pd.read_sql("SELECT * FROM Movies_Companies", conn)

    movies_companies = fillna(movies_companies)
    movies_companies[MOVIE_ID_COLUMN] = movies_companies[MOVIE_ID_COLUMN].astype(
        float).astype(int)

    conn.close()
    if save:
        movies_companies.to_csv(
            f'{path}{EX_MOVIES_COMPANIES_NAME}', index=False)

    return movies_companies


def export_people(path=GENERATED_LOCAL_DIR, save=True):
    conn = sqlite3.connect(DB_LOCAL_PATH)
    people = pd.read_sql("SELECT * FROM People", conn)

    conn.close()
    if save:
        people.to_csv(f'{path}{EX_PEOPLE_NAME}', index=False)

    return people


def export_companies(path=GENERATED_LOCAL_DIR, save=True):
    conn = sqlite3.connect(DB_LOCAL_PATH)
    companies = pd.read_sql("SELECT * FROM Companies", conn)

    conn.close()
    if save:
        companies.to_csv(f'{path}{EX_COMPANIES_NAME}', index=False)

    return companies


def export_all_to_df():
    export_movies()
    export_movies_people()
    export_movies_companies()
    export_people()
    export_companies()


def export_all_to_df_flatten(path=GENERATED_LOCAL_DIR, save=True):
    movies = export_movies(save=False)

    movies_people = export_movies_people(save=False)
    movies_people = movies_people.groupby([MOVIE_ID_COLUMN, CATEGORY_COLUMN])[
        PERSON_ID_COLUMN].agg(lambda x: "|".join(x)).reset_index()
    movies_people = movies_people.pivot(
        index=MOVIE_ID_COLUMN, columns=CATEGORY_COLUMN, values=PERSON_ID_COLUMN).reset_index()

    movies_people.fillna({ACTOR_COLUMN: "", DIRECTOR_COLUMN: ""}, inplace=True)
    movies_people.rename(columns={
                         ACTOR_COLUMN: ACTORS_COLUMN, DIRECTOR_COLUMN: DIRECTORS_COLUMN}, inplace=True)

    movies = movies.merge(movies_people, left_on=IMDB_ID_COLUMN,
                          right_on=MOVIE_ID_COLUMN, how="left")

    movies_companies = export_movies_companies(save=False)

    movies_companies = movies_companies.groupby(MOVIE_ID_COLUMN)[
        COMPANY_ID_COLUMN].agg(lambda x: '|'.join(map(str, x))).reset_index()

    movies_companies.fillna({COMPANY_ID_COLUMN: ""}, inplace=True)

    movies = movies.merge(
        movies_companies, left_on=TMDB_ID_TMDB_COLUMN, right_on=MOVIE_ID_COLUMN, how="left")

    movies = movies[EXPORT_COLUMNS]
    if save:
        movies.to_csv(f'{path}{EX_TMDB_NAME}', index=False)

    return movies


if __name__ == "__main__":
    export_all_to_df_flatten()

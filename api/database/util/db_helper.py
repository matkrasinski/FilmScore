import sqlite3

import pandas as pd

from ...extensions import db
from ..model import *
from ...data.constant.FILES import TMDB_MOVIES_IDS
from ...data.constant.FILES_NAMES import DB_LOCAL_PATH
from ...data.constant.COLUMNS import *


def save_released_movies(data, db_path=DB_LOCAL_PATH):
    data = data.dropna(subset=TMDB_ID_TMDB_COLUMN)
    data = data.drop_duplicates(subset=TMDB_ID_TMDB_COLUMN)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for _, row in data.iterrows():
        tmdb_id = int(row[TMDB_ID_TMDB_COLUMN])
        collection_id = str(int(row[COLLECTION_COLUMN])
                            ) if row[COLLECTION_COLUMN] != "" else ""
        cursor.execute(f'''
        INSERT OR REPLACE INTO Movies ({TMDB_ID_COLUMN}, {IMDB_ID_COLUMN}, {ORIGINAL_TITLE_COLUMN}, {GENRES_COLUMN}, {KEYWORDS_COLUMN},
          {COLLECTION_COLUMN}, {VIDEOS_COLUMN}, {RUNTIME_COLUMN}, {ORIGINAL_LANGUAGE_COLUMN}, {SPOKEN_LANGUAGES_COLUMN}, {STATUS_COLUMN},
            {RELEASE_DATE_COLUMN}, {AVERAGE_RATING_TMDB_COLUMN}, {NUM_VOTES_TMDB_COLUMN})
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (tmdb_id, row[IMDB_ID_COLUMN], row[ORIGINAL_TITLE_COLUMN], row[GENRES_COLUMN],
          row[KEYWORDS_COLUMN], collection_id, row[VIDEOS_COLUMN], row[RUNTIME_COLUMN], row[ORIGINAL_LANGUAGE_COLUMN],
          row[SPOKEN_LANGUAGES_COLUMN], row[STATUS_COLUMN], row[RELEASE_DATE_COLUMN], row[AVERAGE_RATING_IMDB_COLUMN], row[NUM_VOTES_IMDB_COLUMN]))

    conn.commit()
    conn.close()


def save_new_movies(data, db_path=DB_LOCAL_PATH):
    data = data.dropna(subset=TMDB_ID_TMDB_COLUMN)
    data = data.drop_duplicates(subset=TMDB_ID_TMDB_COLUMN)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for _, row in data.iterrows():
        tmdb_id = int(row[TMDB_ID_TMDB_COLUMN])
        collection_id = str(int(row[COLLECTION_COLUMN])
                            ) if row[COLLECTION_COLUMN] != "" else ""
        cursor.execute(f'''
          INSERT OR REPLACE INTO Movies ({TMDB_ID_COLUMN}, {IMDB_ID_COLUMN}, {ORIGINAL_TITLE_COLUMN}, {GENRES_COLUMN}, {KEYWORDS_COLUMN},
          {COLLECTION_COLUMN}, {VIDEOS_COLUMN}, {RUNTIME_COLUMN}, {ORIGINAL_LANGUAGE_COLUMN}, {SPOKEN_LANGUAGES_COLUMN}, {STATUS_COLUMN},
            {RELEASE_DATE_COLUMN}, {PREDICTED_RATING_COLUMN}, {NUM_VOTES_TMDB_COLUMN})
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (tmdb_id, row[IMDB_ID_COLUMN], row[ORIGINAL_TITLE_COLUMN], row[GENRES_COLUMN],
          row[KEYWORDS_COLUMN], collection_id, row[VIDEOS_COLUMN], row[RUNTIME_COLUMN], row[ORIGINAL_LANGUAGE_COLUMN],
          row[SPOKEN_LANGUAGES_COLUMN], row[STATUS_COLUMN], row[RELEASE_DATE_COLUMN], row[PREDICTED_RATING_COLUMN], row[NUM_VOTES_IMDB_COLUMN]))

    conn.commit()
    conn.close()


def save_people(data, db_path=DB_LOCAL_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for _, row in data.iterrows():
        cursor.execute(f'''
          INSERT OR REPLACE INTO People ({PERSON_ID_COLUMN}, {PRIMARY_NAME_TMDB_COLUMN}, {RATING_COLUMN})
          VALUES (?, ?, ?)
      ''', (row[PERSON_COLUMN], row[PRIMARY_NAME_IMDB_COLUMN], row[RATING_COLUMN]))

    conn.commit()
    conn.close()


def save_companies(data, db_path=DB_LOCAL_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for _, row in data.iterrows():
        cursor.execute(f'''
        INSERT OR REPLACE INTO Companies ({COMPANY_ID_COLUMN}, {COMPANY_NAME_COLUMN}, {RATING_COLUMN})
        VALUES (?, ?, ?)
    ''', (row[COMPANY_COLUMN], row[NAME], row[RATING_COLUMN]))

    conn.commit()
    conn.close()


def save_movies_people(data, db_path=DB_LOCAL_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for _, row in data.iterrows():
        for actor in row[ACTORS_COLUMN]:
            cursor.execute(f'''
          INSERT INTO Movies_People ({MOVIE_ID_COLUMN}, {PERSON_ID_COLUMN}, {CATEGORY_COLUMN})
          VALUES (?, ?, ?)
      ''', (row[IMDB_ID_COLUMN], actor, ACTOR_COLUMN))
        for director in row[DIRECTORS_COLUMN]:
            cursor.execute(f'''
          INSERT INTO Movies_People ({MOVIE_ID_COLUMN}, {PERSON_ID_COLUMN}, {CATEGORY_COLUMN})
          VALUES (?, ?, ?)
      ''', (row[IMDB_ID_COLUMN], director, DIRECTOR_COLUMN))

    conn.commit()
    conn.close()


def save_movies_companies(data, db_path=DB_LOCAL_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for _, row in data.iterrows():
        movie_id = str(int(row[ID])) if row[ID] != "" else ""
        for company in row[PRODUCTION_COMPANIES_COLUMN]:

            cursor.execute(f'''
          INSERT INTO Movies_Companies ({MOVIE_ID_COLUMN}, {COMPANY_ID_COLUMN})
          VALUES (?, ?)
      ''', (movie_id, company))

    conn.commit()
    conn.close()


def get_movies(db_path=DB_LOCAL_PATH):
    conn = sqlite3.connect(db_path)

    movies = pd.read_sql("SELECT * FROM Movies", conn)

    conn.close()

    return movies


def get_movies_to_update(db_path=DB_LOCAL_PATH):
    tmdb_new_ids = pd.read_json(TMDB_MOVIES_IDS, lines=True)

    tmdb_new_ids = set(tmdb_new_ids[TMDB_ID_TMDB_COLUMN].to_list())

    conn = sqlite3.connect(db_path)

    movies_ids = pd.read_sql(
        f'SELECT {TMDB_ID_COLUMN}, {STATUS_COLUMN} FROM Movies', conn)

    existing_ids = set(movies_ids[TMDB_ID_COLUMN].astype(int).to_list())

    diff = tmdb_new_ids - existing_ids

    not_relesed = pd.read_sql(
        f'SELECT * FROM Movies WHERE {STATUS_COLUMN} != "Released" or ((1000 - {NUM_VOTES_TMDB_COLUMN}) > 0 and (1000 - {NUM_VOTES_TMDB_COLUMN}) < 10)', conn)

    not_relesed = set(not_relesed[TMDB_ID_COLUMN].astype(int).to_list())

    diff = diff | not_relesed

    conn.close()

    return diff


def delete_movies_people():
    conn = sqlite3.connect(DB_LOCAL_PATH)
    cursor = conn.cursor()

    cursor.execute(f'''
      DELETE FROM Movies_People WHERE {ID} >= 0;
  ''')
    cursor.execute(f'''
      DELETE FROM People WHERE {PERSON_ID_COLUMN} is not null;
  ''')

    conn.commit()


def delete_movies_companies():
    conn = sqlite3.connect(DB_LOCAL_PATH)
    cursor = conn.cursor()

    cursor.execute(f'''
      DELETE FROM Movies_Companies WHERE  >= 0;
  ''')
    cursor.execute(f'''
      DELETE FROM Companies WHERE {COMPANY_ID_COLUMN} is not null;
  ''')

    conn.commit()


def write_image_path(path, id):
    conn = sqlite3.connect(DB_LOCAL_PATH)
    cursor = conn.cursor()

    cursor.execute(f'''
      UPDATE Movies SET {POSTER_SOURCE_COLUMN} = ? WHERE {TMDB_ID_COLUMN} = ?
  ''', (path, id))

    conn.commit()


def save_collections(data):
    conn = sqlite3.connect(DB_LOCAL_PATH)
    cursor = conn.cursor()

    for _, row in data.iterrows():
        cursor.execute(f'''
        INSERT OR REPLACE INTO Collections ({COLLECTION_ID_COLUMN}, {PRIMARY_NAME_TMDB_COLUMN})
        VALUES (?, ?)
    ''', (row[ID], row[NAME]))

    conn.commit()
    conn.close()

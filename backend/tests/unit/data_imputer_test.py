from ...data.util import data_imputer
from ...data.constant.COLUMNS import *
import pandas as pd


def test_filter_data():
    data = pd.read_csv("backend/tests/sample_data/tmdb_sample.csv")
    assert len(data) == 5

    data = prepare_sample_data(data)
    data = prepare_ratings(data)

    assert len(data_imputer.filter_data(data, num_votes_criteria=617351)) == 3


def test_adjust_data():
    data = pd.read_csv("backend/tests/sample_data/tmdb_sample.csv")
    data = prepare_sample_data(data)
    data = prepare_ratings(data)
    data = data_imputer.adjust_data(data)[X_TRAIN_COLUMNS]
    assert not data.isnull().any().any()


def test_prepare_actors():
    actors = data_imputer.prepare_actors(
        "backend/tests/sample_data/title.principals.tsv")
    assert len(actors) == 5


def test_prepare_directors():
    directors = data_imputer.prepare_directors(
        "backend/tests/sample_data/title.crew.tsv")
    assert len(directors) == 5


def test_fillna():
    data = pd.read_csv("backend/tests/sample_data/tmdb_sample.csv")
    data = prepare_sample_data(data)
    data = prepare_ratings(data)
    assert data.isnull().any().any()
    data = data_imputer.fillna(data)
    assert not data.isnull().any().any()


def prepare_sample_data(data):
    imdb_ratings = pd.read_csv(
        "backend/tests/sample_data/title.ratings.tsv", sep="\t")
    data = data.merge(imdb_ratings, left_on=IMDB_ID_COLUMN,
                      right_on=TCONST_COLUMN, how="left")

    directors = data_imputer.prepare_directors(
        title_crew="backend/tests/sample_data/title.crew.tsv")

    data = data.merge(directors, left_on=IMDB_ID_COLUMN,
                      right_on=TCONST_COLUMN, how="left")

    actors = data_imputer.prepare_actors(
        title_principals="backend/tests/sample_data/title.principals.tsv")
    data = data.merge(actors, left_on=IMDB_ID_COLUMN,
                      right_on=TCONST_COLUMN, how="left")

    return data


def prepare_ratings(data):
    data["actors_rating"] = 0.6
    data["directors_rating"] = 0.6
    data["companies_rating"] = 0.6
    return data


print(test_prepare_actors())

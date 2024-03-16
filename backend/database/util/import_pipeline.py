import numpy as np
import pandas as pd

from ...ai.model_loader import ModelLoader
from ...database.util import db_helper
from ...data.constant.FILES import TITLE_RATINGS, TMDB_COLLECTIONS, TMDB_DATA, TITLE_CREW, TITLE_PRINCIPALS
from ...data.constant.FILES_NAMES import KNN_MODEL_LOCAL_PATH
from ...data.constant.COLUMNS import *
from ...data.util.ratings_generator import RatingsGenerator
from ...data.util.data_imputer import prepare_actors, prepare_directors, fillna, fillna_ratings, replace_keywords_sep, filter_data, adjust_data


class ImportPipeline:
    def __init__(self, data={}, train_data={}, new_data={}):
        self.ratings_helper = RatingsGenerator()
        self.data = data
        self.train_data = train_data
        self.new_data = new_data

    def get_data(self, how="left", tmdb_data=TMDB_DATA, title_ratings=TITLE_RATINGS, title_crew=TITLE_CREW, principals=TITLE_PRINCIPALS):
        self.data = pd.read_csv(tmdb_data)
        self.data.reset_index(drop=True)

        imdb_ratings = pd.read_csv(title_ratings, sep="\t")
        self.data = self.data.merge(
            imdb_ratings, left_on=IMDB_ID_COLUMN, right_on=TCONST_COLUMN, how=how)

        self.directors = prepare_directors(title_crew=title_crew)
        self.data = self.data.merge(
            self.directors, left_on=IMDB_ID_COLUMN, right_on=TCONST_COLUMN, how=how)

        self.actors = prepare_actors(title_principals=principals)
        self.data = self.data.merge(
            self.actors, left_on=IMDB_ID_COLUMN, right_on=TCONST_COLUMN, how=how)

        print("merge_tmdb_imdb : Done")

        return self

    def set_released_data(self):
        self.data = self.data[self.data[STATUS_COLUMN] == "Released"]
        self.data = fillna(self.data)
        self.data = replace_keywords_sep(self.data)

        print("set_released_data : Done")
        return self

    def set_new_data(self):
        self.new_data = self.data[self.data[STATUS_COLUMN] != "Released"]
        self.new_data = fillna(self.new_data)
        self.new_data = self.apply_ratings(self.new_data)
        self.new_data = fillna_ratings(self.new_data, )
        self.new_data = replace_keywords_sep(self.new_data)

        print("set_new_data : Done")
        return self

    def set_train_data(self):
        self.train_data = self.data[self.data[STATUS_COLUMN] == "Released"]
        self.train_data = filter_data(self.train_data)
        self.train_data = adjust_data(self.train_data)

        self.ratings_helper.generate_companies_ratings(self.train_data)
        self.ratings_helper.generate_people_ratings(self.train_data)

        # require ratings generated
        self.train_data = fillna(self.train_data)
        self.train_data = self.apply_ratings(self.train_data)

        people_med = np.median([*self.ratings_helper.people_ratings.values()])
        companies_ratings_med = np.median(
            [*self.ratings_helper.companies_ratings.values()])

        self.train_data = fillna_ratings(
            self.train_data, actors_rating=people_med, directors_rating=people_med, companies_ratings=companies_ratings_med)
        self.train_data = replace_keywords_sep(self.train_data)

        print("set_train_data : Done")
        return self

    def apply_ratings(self, data):
        people_ratings = self.ratings_helper.people_ratings

        data[DIRECTORS_RATING_COLUMN] = data[DIRECTORS_COLUMN].apply(lambda x: np.mean(
            [people_ratings[director] for director in x if director in people_ratings]))
        data[ACTORS_RATING_COLUMN] = data[ACTORS_COLUMN].apply(lambda x: np.mean(
            [people_ratings[actor] for actor in x if actor in people_ratings]))

        companies_ratings = self.ratings_helper.companies_ratings
        data[COMPANIES_RATING_COLUMN] = data[PRODUCTION_COMPANIES_COLUMN].apply(lambda x: np.mean(
            [companies_ratings[company] for company in x if company in companies_ratings]))

        print("apply_ratings : Done")
        return data

    def save_released_movies(self):
        to_save = self.data
        to_save[GENRES_COLUMN] = to_save[GENRES_COLUMN].apply(
            lambda x: "|".join(x))
        to_save[SPOKEN_LANGUAGES_COLUMN] = to_save[SPOKEN_LANGUAGES_COLUMN].apply(
            lambda x: "|".join(x))
        to_save.dropna(subset=TMDB_ID_TMDB_COLUMN, inplace=True)
        to_save.fillna({
            ORIGINAL_TITLE_COLUMN: "",
            PREDICTED_RATING_COLUMN: 0,
            POSTER_SOURCE_COLUMN: ""
        }, inplace=True)

        db_helper.save_released_movies(to_save)
        db_helper.save_movies_people(to_save)
        db_helper.save_movies_companies(to_save)

        print("save_released_movies : Done")
        return self

    def run_predictions(self, model_path=KNN_MODEL_LOCAL_PATH):
        new_data_copy = self.new_data.copy()
        new_data_copy[RELEASE_DATE_COLUMN] = new_data_copy[RELEASE_DATE_COLUMN].apply(
            lambda x: x if x != "" else "9999-12-31")

        self.new_data[PREDICTED_RATING_COLUMN] = ModelLoader(
            model_path=model_path, train_data=self.train_data).predict_rating(new_data_copy)
        return self

    def save_new_movies(self):
        to_save = self.new_data
        to_save[GENRES_COLUMN] = to_save[GENRES_COLUMN].apply(
            lambda x: "|".join(x))
        to_save[SPOKEN_LANGUAGES_COLUMN] = to_save[SPOKEN_LANGUAGES_COLUMN].apply(
            lambda x: "|".join(x))
        to_save.dropna(subset=TMDB_ID_TMDB_COLUMN, inplace=True)

        db_helper.save_new_movies(to_save)
        db_helper.save_movies_people(to_save)
        db_helper.save_movies_companies(to_save)
        return self

    def save_people(self):
        db_helper.save_people(self.ratings_helper.people_ratings_to_df())
        return self

    def save_companies(self):
        db_helper.save_companies(self.ratings_helper.companies_ratings_to_df())
        return self

    def save_collections(self):
        collections = pd.read_json(TMDB_COLLECTIONS, lines=True)
        db_helper.save_collections(collections)
        return self

    def run_pipeline(self):
        self.get_data()\
            .set_train_data()\
            .set_new_data()\
            .set_released_data()\
            .save_companies()\
            .save_people()\
            .save_collections()\
            .save_released_movies()\
            .run_predictions()\
            .save_new_movies()

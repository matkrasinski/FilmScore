import numpy as np
import pandas as pd

from ...ai.model_loader import ModelLoader
from ...data.image_selector import find_image
from ..util import db_helper
from ...data.util.ratings_generator import RatingsGenerator
from ...data.constant.FILES import *
from ...data.util.api_data_fetcher import get_movie_data
from ...data.constant.COLUMNS import *
from ...data.util.data_exporter import export_all_to_df_flatten
from ...data.util.data_imputer import fillna, fillna_ratings, adjust_data, filter_data, replace_keywords_sep


class UpdatePipeline:

    def __init__(self, data={}, train_data={}, new_data={}):
        self.ratings_helper = RatingsGenerator()
        self.data = data
        self.train_data = train_data
        self.new_data = new_data

    def init_imdb(self, title_ratings=TITLE_RATINGS):
        self.imdb_ratings = pd.read_csv(title_ratings, sep="\t")
        print("IMDB INITIALIZED")
        return self

    def update_data(self, max_size=None):
        ids_to_update = db_helper.get_movies_to_update()

        batch_size = 100
        updated_data = []
        ids = []
        for id in ids_to_update:
            ids.append(id)
            new_data = get_movie_data(id)

            if len(new_data) != 0:
                updated_data.append(new_data)

            if len(updated_data) == batch_size:
                to_save = pd.DataFrame(updated_data)
                to_save = to_save.merge(
                    self.imdb_ratings, left_on=IMDB_ID_COLUMN, right_on=TCONST_COLUMN, how="left")
                db_helper.save_released_movies(to_save)
                print(len(ids))
                updated_data.clear()

            if max_size is not None and len(ids) >= max_size:
                break

        print("UPDATE FINISHED")
        return self

    def drop_prev_movies_people(self):
        db_helper.delete_movies_people()
        print("MOVIES_PEOPLE DROPPED")
        return self

    def drop_prev_movies_companies(self):
        db_helper.delete_movies_companies()
        print("MOVIES_Companies DROPPED")
        return self

    def set_data(self):
        self.data = export_all_to_df_flatten(save=False)
        # self.data = adjust_data(self.data)
        self.data.rename(columns={
            AVERAGE_RATING_TMDB_COLUMN: AVERAGE_RATING_IMDB_COLUMN,
            NUM_VOTES_TMDB_COLUMN: NUM_VOTES_IMDB_COLUMN,
            TMDB_ID_COLUMN: TMDB_ID_TMDB_COLUMN
        }, inplace=True)
        print("DATA SET")
        print(self.data[self.data[STATUS_COLUMN] != "Released"])

        return self

    def set_train_data(self):
        self.train_data = self.data[self.data[STATUS_COLUMN] == "Released"]
        self.train_data = filter_data(self.train_data)
        self.train_data = adjust_data(self.train_data)

        self.ratings_helper.generate_companies_ratings(self.train_data)

        print(self.train_data)
        self.ratings_helper.generate_people_ratings(self.train_data)

        self.train_data = fillna(self.train_data)
        self.train_data = self.apply_ratings(self.train_data)
        self.train_data = fillna_ratings(self.train_data)
        self.train_data = replace_keywords_sep(self.train_data)

        print("TRAIN DATA SET")

        return self

    def set_new_data(self):
        self.new_data = self.data[self.data[STATUS_COLUMN] != "Released"]
        self.new_data = fillna(self.new_data)
        self.new_data = self.apply_ratings(self.new_data)
        self.new_data = fillna_ratings(self.new_data)
        self.new_data = replace_keywords_sep(self.new_data)

        print(self.new_data)
        print("set_new_data : Done")
        return self

    def set_released_data(self):
        self.data = self.data[self.data[STATUS_COLUMN] == "Released"]
        self.data = fillna(self.data)
        self.data = replace_keywords_sep(self.data)

        print("set_released_data : Done")
        return self

    def apply_ratings(self, data):
        people_ratings = self.ratings_helper.people_ratings
        companies_ratings = self.ratings_helper.companies_ratings

        data[DIRECTORS_RATING_COLUMN] = data[DIRECTORS_COLUMN].apply(lambda x: np.mean(
            [people_ratings[director] for director in x if director in people_ratings]))
        data[ACTORS_RATING_COLUMN] = data[ACTORS_COLUMN].apply(lambda x: np.mean(
            [people_ratings[actor] for actor in x if actor in people_ratings]))
        data[COMPANIES_RATING_COLUMN] = data[PRODUCTION_COMPANIES_COLUMN].apply(lambda x: np.mean(
            [companies_ratings[company] for company in x if company in companies_ratings]))

        print("apply_ratings : Done")
        return data

    def save_people(self):
        db_helper.save_people(self.ratings_helper.people_ratings_to_df())
        print("PEOPLE SAVED")
        return self

    def save_companies(self):
        db_helper.save_companies(self.ratings_helper.companies_ratings_to_df())
        print("COMPANIES SAVED")
        return self

    def save_released_movies(self):
        to_save = self.data
        to_save[GENRES_COLUMN] = to_save[GENRES_COLUMN].apply(
            lambda x: "|".join(x) if isinstance(x, list) else x)
        to_save[SPOKEN_LANGUAGES_COLUMN] = to_save[SPOKEN_LANGUAGES_COLUMN].apply(
            lambda x: "|".join(x) if isinstance(x, list) else x)
        to_save.dropna(subset=TMDB_ID_TMDB_COLUMN, inplace=True)
        to_save.fillna({
            "original_title": "",
            "predicted_rating": 0,
        }, inplace=True)

        to_save[POSTER_SOURCE_COLUMN] = to_save.apply(
            lambda x: find_image(x[TMDB_ID_TMDB_COLUMN]))

        db_helper.save_released_movies(to_save)
        db_helper.save_movies_people(to_save)
        db_helper.save_movies_companies(to_save)

        print("save_released_movies : Done")
        return self

    def run_predictions(self):
        print(self.new_data)
        if len(self.new_data) != 0:
            new_data_copy = self.new_data.copy()
            new_data_copy[RELEASE_DATE_COLUMN] = new_data_copy[RELEASE_DATE_COLUMN].apply(
                lambda x: x if x != "" else "9999-12-31")
            self.new_data[PREDICTED_RATING_COLUMN] = ModelLoader(
                train_data=self.train_data).predict_rating(new_data_copy)
        print("PREDICTIONS DONE")
        return self

    def save_new_movies(self):
        to_save = self.new_data
        to_save[GENRES_COLUMN] = to_save[GENRES_COLUMN].apply(
            lambda x: "|".join(x) if isinstance(x, list) else x)
        to_save[SPOKEN_LANGUAGES_COLUMN] = to_save[SPOKEN_LANGUAGES_COLUMN].apply(
            lambda x: "|".join(x) if isinstance(x, list) else x)
        to_save.dropna(subset=TMDB_ID_TMDB_COLUMN, inplace=True)

        db_helper.save_new_movies(to_save)
        db_helper.save_movies_people(to_save)
        db_helper.save_movies_companies(to_save)

        print("NEW MOVIES SAVED")
        return self

    def run_pipeline(self):
        self.init_imdb()\
            .update_data(max_size=100)\
            .set_data()\
            .set_train_data()\
            .set_new_data()\
            .save_companies()\
            .save_people()\
            .run_predictions()\
            .save_new_movies()

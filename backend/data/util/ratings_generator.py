import numpy as np
import pandas as pd

from ...database.model import People, Companies
from ...data.constant.COLUMNS import *
from ...data.constant.FILES_NAMES import GENERATED_LOCAL_DIR, PEOPLE_RATINGS_NAME, COMPANIES_RATINGS_NAME
from ...data.constant.FILES import NAMES_BASICS, TMDB_COMPANIES_IDS
from sqlalchemy import func


class RatingsGenerator:
    people_ratings = {}
    companies_ratings = {}

    def __init__(self, people_ratings={}, companies_ratings={}):
        self.people_ratings = people_ratings
        self.companies_ratings = companies_ratings
        pass

    def generate_companies_ratings(self, data, actor_weight=1, movies_num_weight=0.15, num_votes_weight=0.55, force=False):
        if len(self.companies_ratings) != 0 and not force:
            return self.companies_ratings

        first_set = set()
        second_set = set()
        third_set = set()
        self.companies_ratings = {}

        for _, row in data.iterrows():
            for company in row[PRODUCTION_COMPANIES_COLUMN]:
                if company in self.companies_ratings:
                    self.companies_ratings[company][0] += row[AVERAGE_RATING_IMDB_COLUMN]
                    self.companies_ratings[company][1] += row[NUM_VOTES_IMDB_COLUMN]
                    self.companies_ratings[company][2] += 1
                else:
                    self.companies_ratings[company] = [
                        row[AVERAGE_RATING_IMDB_COLUMN], row[NUM_VOTES_IMDB_COLUMN], 1]

        for company in self.companies_ratings:
            self.companies_ratings[company][0] = self.companies_ratings[company][0] / \
                self.companies_ratings[company][2]
            first_set.add(self.companies_ratings[company][0])
            third_set.add(self.companies_ratings[company][1])
            second_set.add(self.companies_ratings[company][2])

        first = (min(first_set), max(first_set))
        second = (min(second_set), max(second_set))
        third = (min(third_set), max(third_set))

        for company in self.companies_ratings:
            self.companies_ratings[company][0] = normalize_feature(
                self.companies_ratings[company][0], first[0], first[1])
            self.companies_ratings[company][1] = normalize_feature(
                self.companies_ratings[company][1], third[0], third[1])
            self.companies_ratings[company][2] = normalize_feature(
                self.companies_ratings[company][2], second[0], second[1])

        for company in self.companies_ratings:
            self.companies_ratings[company] = (self.companies_ratings[company][0] * actor_weight) + (
                self.companies_ratings[company][2] * movies_num_weight) + (self.companies_ratings[company][1] * num_votes_weight)

        return self.companies_ratings

    def generate_people_ratings(self, data, actor_weight=1, movies_num_weight=0.15, num_votes_weight=0.55, force=False):
        if len(self.people_ratings) != 0 and not force:
            return self.people_ratings

        first_set = set()
        second_set = set()
        third_set = set()
        self.people_ratings = {}

        for _, row in data.iterrows():
            for director in row[DIRECTORS_COLUMN]:
                if director in self.people_ratings:
                    self.people_ratings[director][0] += row[AVERAGE_RATING_IMDB_COLUMN]
                    self.people_ratings[director][1] += row[NUM_VOTES_IMDB_COLUMN]
                    self.people_ratings[director][2] += 1
                else:
                    self.people_ratings[director] = [
                        row[AVERAGE_RATING_IMDB_COLUMN], row[NUM_VOTES_IMDB_COLUMN], 1]

            for actor in row[ACTORS_COLUMN]:
                if actor in self.people_ratings:
                    self.people_ratings[actor][0] += row[AVERAGE_RATING_IMDB_COLUMN]
                    self.people_ratings[actor][1] += row[NUM_VOTES_IMDB_COLUMN]
                    self.people_ratings[actor][2] += 1
                else:
                    self.people_ratings[actor] = [
                        row[AVERAGE_RATING_IMDB_COLUMN], row[NUM_VOTES_IMDB_COLUMN], 1]

        for person in self.people_ratings:
            self.people_ratings[person][0] = self.people_ratings[person][0] / \
                self.people_ratings[person][2]
            first_set.add(self.people_ratings[person][0])
            third_set.add(self.people_ratings[person][1])
            second_set.add(self.people_ratings[person][2])

        first = (min(first_set), max(first_set))
        second = (min(second_set), max(second_set))
        third = (min(third_set), max(third_set))

        for person in self.people_ratings:
            self.people_ratings[person][0] = normalize_feature(
                self.people_ratings[person][0], first[0], first[1])
            self.people_ratings[person][1] = normalize_feature(
                self.people_ratings[person][1], third[0], third[1])
            self.people_ratings[person][2] = normalize_feature(
                self.people_ratings[person][2], second[0], second[1])

        for person in self.people_ratings:
            self.people_ratings[person] = (self.people_ratings[person][0] * actor_weight) + (
                self.people_ratings[person][2] * movies_num_weight) + (self.people_ratings[person][1] * num_votes_weight)

        return self.people_ratings

    def people_ratings_to_df(self, generated_path=GENERATED_LOCAL_DIR, save=True):
        people_ratings_df = pd.DataFrame(list(self.people_ratings.items()), columns=[
                                         PERSON_COLUMN, RATING_COLUMN])
        people_ratings_df.columns = [PERSON_COLUMN, RATING_COLUMN]

        names = pd.read_csv(NAMES_BASICS, sep="\t")

        people_ratings_df = people_ratings_df.merge(names, left_on=PERSON_COLUMN, right_on=NCONST_COLUMN, how="left")[
            [PERSON_COLUMN, PRIMARY_NAME_IMDB_COLUMN, RATING_COLUMN]]

        if save:
            people_ratings_df.sort_values(by=RATING_COLUMN, ascending=False).to_csv(
                f'{generated_path}{PEOPLE_RATINGS_NAME}', index=False)


        return people_ratings_df

    def companies_ratings_to_df(self, generated_path=GENERATED_LOCAL_DIR, save=True):
        companies_ratings_df = pd.DataFrame(
            list(self.companies_ratings.items()), columns=[COMPANY_COLUMN, RATING_COLUMN])

        companies_ratings_df.columns = [COMPANY_COLUMN, RATING_COLUMN]
        
        companies_ratings_df[COMPANY_COLUMN] = companies_ratings_df[COMPANY_COLUMN].apply(
            lambda x: int(x) if x != '' else x)

        names = pd.read_json(TMDB_COMPANIES_IDS, lines=True)

        companies_ratings_df = companies_ratings_df.merge(
            names, left_on=COMPANY_COLUMN, right_on=ID, how="right")[[ID, NAME, RATING_COLUMN]]
        companies_ratings_df.fillna({RATING_COLUMN: -1}, inplace=True)
        companies_ratings_df.rename(columns={ID: COMPANY_COLUMN}, inplace=True)

        if save:
            companies_ratings_df.sort_values(by=RATING_COLUMN, ascending=False).to_csv(
                f'{generated_path}{COMPANIES_RATINGS_NAME}', index=False)

        return companies_ratings_df

    def get_people_avg_ratings(self, people=[]):
        people_ratings = People.query.filter(
            People.person_id.in_(people)).with_entities(People.rating).all()

        return np.mean(people_ratings)

    def get_companies_avg_ratings(self, companies=[]):
        companies_ratings = Companies.query.filter(
            Companies.company_id.in_(companies)).with_entities(Companies.rating).all()

        return np.mean(companies_ratings)

    def get_people_ratings_med(self):
        people_ratings = People.query.filter(
            People.rating >= 0).with_entities(People.rating).all()
        people_ratings = np.median(list(map(lambda x: x[0], people_ratings)))

        return people_ratings

    def get_companies_ratings_med(self):
        companies_ratings = Companies.query.filter(Companies.rating >= 0).with_entities(
            Companies.rating).all()
        companies_ratings = np.median(
            list(map(lambda x: x[0], companies_ratings)))
        return companies_ratings


def normalize_feature(value, min, max):
    diff = max - min
    if diff == 0:
        diff = 1
    return (value - min) / diff

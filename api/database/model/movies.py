from api.extensions import db
import numpy as np
from ...data.constant.COLUMNS import *


class Movies(db.Model):
    __tablename__ = "Movies"
    tmdb_id = db.Column(db.String(255), primary_key=True)

    imdb_id = db.Column(db.String(255))
    original_title = db.Column(db.String(255))
    genres = db.Column(db.String(255))
    average_rating = db.Column(db.Float)
    predicted_rating = db.Column(db.Float)
    num_votes = db.Column(db.Integer)
    keywords = db.Column(db.String(4096))
    belongs_to_collection = db.Column(
        db.String(255), db.ForeignKey('Collections.collection_id'))
    videos = db.Column(db.String(4096))
    runtime = db.Column(db.Float)
    original_language = db.Column(db.String(255))
    spoken_languages = db.Column(db.String(255))
    status = db.Column(db.String(255))
    release_date = db.Column(db.String(255))

    poster_source = db.Column(db.String(255))

    people = db.relationship("MoviesPeople", back_populates='movie')
    companies = db.relationship("MoviesCompanies", back_populates='movie')

    def __init__(self, tmdb_id, imdb_id, original_title, genres,
                 num_votes, keywords, belongs_to_collection, videos, runtime, original_language,
                 spoken_languages, release_date, status,
                 average_rating=0.0, predicted_rating=0.0, poster_source="", people=[], companies=[]):
        self.tmdb_id = tmdb_id
        self.imdb_id = imdb_id
        self.original_title = original_title
        self.genres = genres
        self.average_rating = average_rating
        self.predicted_rating = predicted_rating
        self.num_votes = num_votes
        self.keywords = keywords
        self.belongs_to_collection = belongs_to_collection
        self.videos = videos
        self.runtime = runtime
        self.original_language = original_language
        self.spoken_languages = spoken_languages
        self.release_date = release_date
        self.poster_source = poster_source
        self.people = people
        self.companies = companies
        self.status = status

    def to_large_dict(self):
        print(self.people, self.companies)
        actors = list(map(lambda x: {ID: x.person.person_id, NAME: x.person.primary_name}, filter(
            lambda x: x.category == ACTOR_COLUMN and x.person is not None, self.people)))
        directors = list(map(lambda x:  {ID: x.person.person_id, NAME: x.person.primary_name}, filter(
            lambda x: x.category == DIRECTOR_COLUMN and x.person is not None, self.people)))
        companies = list(map(lambda x:  {ID: x.company.company_id, NAME: x.company.company_name}, filter(
            lambda x: x.company is not None, self.companies)))

        return {
            TMDB_ID_COLUMN: self.tmdb_id,
            IMDB_ID_COLUMN: self.imdb_id,
            ORIGINAL_TITLE_COLUMN: self.original_title,
            GENRES_COLUMN: self.genres.split("|") if isinstance(self.genres, str) else [],
            AVERAGE_RATING_TMDB_COLUMN: self.average_rating,
            PREDICTED_RATING_COLUMN: self.predicted_rating,
            NUM_VOTES_TMDB_COLUMN: self.num_votes,
            KEYWORDS_COLUMN: self.keywords.replace("|", " ") if isinstance(self.keywords, str) else "",
            COLLECTION_COLUMN: self.belongs_to_collection,
            VIDEOS_COLUMN: self.videos,
            RUNTIME_COLUMN: self.runtime,
            ORIGINAL_LANGUAGE_COLUMN: self.original_language,
            SPOKEN_LANGUAGES_COLUMN: self.spoken_languages.split("|") if isinstance(self.spoken_languages, str) else [],
            STATUS_COLUMN: self.status,
            RELEASE_DATE_COLUMN: self.release_date,

            POSTER_SOURCE_COLUMN: self.poster_source,

            ACTORS_COLUMN: actors,
            DIRECTORS_COLUMN: directors,
            PRODUCTION_COMPANIES_COLUMN: companies
        }

    def to_dict(self):
        return {
            TMDB_ID_COLUMN: self.tmdb_id,
            IMDB_ID_COLUMN: self.imdb_id,
            ORIGINAL_TITLE_COLUMN: self.original_title,
            GENRES_COLUMN: self.genres.split("|") if isinstance(self.genres, str) else [],
            AVERAGE_RATING_TMDB_COLUMN: self.average_rating,
            PREDICTED_RATING_COLUMN: self.predicted_rating,
            NUM_VOTES_TMDB_COLUMN: self.num_votes,
            KEYWORDS_COLUMN: self.keywords.replace("|", " ") if isinstance(self.keywords, str) else "",
            COLLECTION_COLUMN: self.belongs_to_collection,
            VIDEOS_COLUMN: self.videos,
            RUNTIME_COLUMN: self.runtime,
            ORIGINAL_LANGUAGE_COLUMN: self.original_language,
            SPOKEN_LANGUAGES_COLUMN: self.spoken_languages.split("|") if isinstance(self.spoken_languages, str) else [],
            STATUS_COLUMN: self.status,
            RELEASE_DATE_COLUMN: self.release_date,

            POSTER_SOURCE_COLUMN: self.poster_source,
        }

    def to_small_dict(self):
        return {
            TMDB_ID_COLUMN: self.tmdb_id,
            IMDB_ID_COLUMN: self.imdb_id,
            ORIGINAL_TITLE_COLUMN: self.original_title,
            AVERAGE_RATING_TMDB_COLUMN: self.average_rating,
            PREDICTED_RATING_COLUMN: self.predicted_rating,
            RELEASE_DATE_COLUMN: self.release_date,
            POSTER_SOURCE_COLUMN: self.poster_source,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update_movie(self, prediction):
        self.predicted_rating = prediction
        db.session.commit()

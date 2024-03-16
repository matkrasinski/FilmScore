import json
import math
from datetime import date
from itertools import chain
from flask import jsonify
import pandas as pd
from flask import Blueprint, request
from sqlalchemy import func

from ..data.image_selector import find_image
from ..database.util import db_helper
from ..extensions import db
from .model.collections import Collections
from .model.companies import Companies
from .model.movies import Movies
from .model.people import People

db_bp = Blueprint("db", __name__, url_prefix="/db")


@db_bp.route("/movies/pages", methods=['POST'])
def _find_movies():
    page = int(request.args.get("page"))
    size = int(request.args.get("size"))
    query = request.args.get("query")
    body = request.get_json()
    genres = body[0]

    sort_by = body[1]

    genre_conditions = [Movies.genres.like(f"%{genre}%") for genre in genres]

    offset = page * size

    order_conditions = []
    if "numVotes" in sort_by.keys() and sort_by["numVotes"] == "desc":
        order_conditions.append(Movies.num_votes.desc())
    elif "numVotes" in sort_by.keys() and sort_by["numVotes"] == "asc":
        order_conditions.append(Movies.num_votes.asc())

    if "rating" in sort_by.keys() and sort_by["rating"] == "desc":
        order_conditions.append(Movies.average_rating.desc())
    elif "rating" in sort_by.keys() and sort_by["rating"] == "asc":
        order_conditions.append(Movies.average_rating.asc())

    movies_query = Movies.query.filter(Movies.status == "Released", *genre_conditions, func.lower(
        Movies.original_title).like(f'%{query}%')).order_by(*order_conditions)

    movies = {'movies': [item.to_small_dict()
                         for item in movies_query.limit(size).offset(offset).all()]}

    count = movies_query.count()
    movies["max_size"] = math.ceil(count / size)

    return jsonify(movies)


@db_bp.route("/movies/new/pages", methods=["POST"])
def _find_new_movies():
    page = int(request.args.get("page"))
    size = int(request.args.get("size"))
    query = request.args.get("query")

    body = request.get_json()
    genres = body[0]

    sort_by = body[1]

    offset = page * size
    current_date = date.today()
    order_conditions = []
    if "numVotes" in sort_by.keys() and sort_by["numVotes"] == "desc":
        order_conditions.append(Movies.num_votes.desc())
    elif "numVotes" in sort_by.keys() and sort_by["numVotes"] == "asc":
        order_conditions.append(Movies.num_votes.asc())

    if "rating" in sort_by.keys() and sort_by["rating"] == "desc":
        order_conditions.append(Movies.predicted_rating.desc())
    elif "rating" in sort_by.keys() and sort_by["rating"] == "asc":
        order_conditions.append(Movies.predicted_rating.asc())
    order_conditions.append(func.abs(Movies.release_date - current_date))
    genre_conditions = [Movies.genres.like(f"%{genre}%") for genre in genres]

    movies_query = Movies.query.filter(Movies.status != "Released",
                                       *genre_conditions,
                                       func.lower(Movies.original_title).like(f'%{query}%'))\
        .order_by(*order_conditions)

    movies = {'movies': [item.to_small_dict()
                         for item in movies_query.limit(size).offset(offset).all()]}
    count = movies_query.count()

    movies["max_size"] = math.ceil(count / size)
    return jsonify(movies)


@db_bp.route("/image", methods=["GET"])
def _get_image():
    id = request.args.get("id")
    path = find_image(id, save=True)
    if path is not None:
        db_helper.write_image_path(path, id)
    else:
        db_path = Movies.query.filter(Movies.tmdb_id == id).with_entities(
            Movies.poster_source).first()[0]
        path = db_path if db_path != "" else None
    print(path)
    return jsonify(path)


@db_bp.route("/people", methods=["GET"])
def _get_people():
    movies = People.query.order_by(People.rating).all()
    return jsonify([item.to_dict() for item in movies])


@db_bp.route("/genres", methods=["GET"])
def _get_genres():
    genres = ['Mystery', 'Fantasy', 'Adventure',
              'Thriller', 'History', 'Documentary',
              'Crime', 'Comedy', 'Horror',
              'Family', 'Western', 'Romance',
              'Music', 'Action', 'TV Movie',
              'War', 'Drama', 'Animation', 'Science Fiction']

    return jsonify(genres)


@db_bp.route("/og_langs", methods=["GET"])
def _get_langs():
    all_languages = Movies.query.with_entities(Movies.original_language).all()
    unique_langs = set(map(lambda lang: lang[0], all_languages))

    return jsonify(list(unique_langs))


@db_bp.route("/collections", methods=["GET"])
def _get_collections():
    collections = Collections.query.all()
    collections = [collection.to_dict() for collection in collections]

    return jsonify(collections)


@db_bp.route("/spoken_languages", methods=["GET"])
def _get_spoken_languages():
    spoken_languages = Movies.query.with_entities(
        Movies.spoken_languages).all()
    spoken_languages = list(
        map(lambda lang: lang[0].split("|"), spoken_languages))
    spoken_languages = list(chain(*spoken_languages))
    spoken_languages = set(spoken_languages)

    return jsonify(list(spoken_languages))


@db_bp.route("/companies", methods=["GET"])
def _get_production_companies():
    all_companies = Companies.query.all()
    all_companies = [company.to_simple_dict() for company in all_companies]

    return jsonify(all_companies)


@db_bp.route("/movie", methods=["GET"])
def _get_movie_data():
    id = request.args.get("id")

    movie = Movies.query.filter(Movies.tmdb_id == id).first()

    return jsonify(movie.to_large_dict())

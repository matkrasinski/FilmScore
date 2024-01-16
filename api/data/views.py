from flask import Blueprint, request
from .data_manager import check_data_status, get_people, get_genres, get_companies, get_languages, get_all_movies, get_image, get_paged_released_movies, get_paged_new_movies

import json

data_bp = Blueprint("data", __name__, url_prefix="/data")

@data_bp.route("/status", methods=["GET"])
def check_status():
  status = check_data_status()
  print(status)
  return json.dumps(status)

@data_bp.route("/people", methods=["GET"])
def get_people_ratings():
  people = get_people()
  return json.dumps(people)

@data_bp.route("/genres", methods=["GET"])
def _get_genres():
  genres = get_genres()
  return json.dumps(genres)

@data_bp.route("/companies", methods=["GET"])
def _get_companies():
  companies = get_companies()
  return json.dumps(companies)

@data_bp.route("/languages", methods=["GET"])
def _get_languages():
  languages = get_languages()

  return json.dumps(languages)


@data_bp.route("/movies", methods=["GET"])
def _get_all_movies():
  movies = get_all_movies()

  return json.dumps(movies)

@data_bp.route("/movies/pages", methods=["GET"])
def _find_movies():
  page = int(request.args.get("page"))
  size = int(request.args.get("size"))
  movies = get_paged_released_movies(page, size)
  print(len(movies))

  return json.dumps(movies)

@data_bp.route("/movies/new/pages", methods=["GET"])
def _find_new_movies():
  page = int(request.args.get("page"))
  size = int(request.args.get("size"))
  movies = get_paged_new_movies(page, size)
  print(len(movies))

  return json.dumps(movies)


@data_bp.route("/image", methods=["GET"])
def _get_image():
  id = request.args.get("id")
  path = get_image(id)
  print(path)
  return json.dumps(path)
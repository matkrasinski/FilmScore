from flask import Blueprint
from .data_manager import check_data_status, get_people, get_genres, get_companies, get_languages

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
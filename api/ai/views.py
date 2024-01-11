from flask import Blueprint
from .model_loader import generate_model, predict_rating
import pandas as pd
ai_bp = Blueprint("ai", __name__, url_prefix="/model")

@ai_bp.route("/predict", methods=["GET"])
def predict():
  # TODO 

  data = {
    "belongs_to_collection": "",
    "genres": ['Drama', 'History'],
    "id": "872585",		
    "imdb_id": 'tt15398776',
    "original_language": "",
    "release_date": "2023-07-19",
    "production_companies": ['Syncopy', 'Universal Pictures', 'Atlas Entertainment'],
    "runtime": 181,
    "spoken_languages": ['Nederlands', 'English'],
    "status": "Released",
    "keywords": 'based on novel or book husband wife relationship new mexico patriotism atomic bomb world war ii atomic bomb test biography physics politics physicist based on true story jewish american guilt nuclear weapons communism red scare prometheus mccarthyism 1940s ethics new mexico desert 20th century manhattan project affair los alamos',
    "videos": "Yours to Own Promo|Oppenheimer 70mm film reel running in the BFI IMAX|Oppenheimer's cast on their first viewing of Christopher Nolan's film|Get Tickets NOW|Christopher Nolan, Cillian Murphy, Emily Blunt and Matt Damon on Oppenheimer|Matt Damon, Emily Blunt and Cillian Murphy Discuss Oppenheimer|The Score|Trinity Test|UK Premiere|Opening Look|Christopher Nolan & Cast Interviews|The Cast|Pushing The Button|Shooting For IMAX|New Trailer|Official Trailer",
    "actors": [],
    "directors": ['nm0634241']
  }
  data = pd.DataFrame([data])
  print(data)

  return {"prediction" :predict_rating(data)}

@ai_bp.route("/generate", methods=["GET"])
def generate():
  print("RUNNING")
  generate_model()
  return "Generating"
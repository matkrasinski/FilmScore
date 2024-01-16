from flask import Blueprint, request
from .model_loader import generate_model, predict_rating
import pandas as pd
ai_bp = Blueprint("ai", __name__, url_prefix="/model")


@ai_bp.route("/predict", methods=["POST"])
def predict():
  body = request.get_json()
  data = pd.DataFrame([body])
  print(data)

  return {"prediction" :predict_rating(data)[0]}

@ai_bp.route("/generate", methods=["GET"])
def generate():
  print("RUNNING")
  generate_model()
  return "Generating"
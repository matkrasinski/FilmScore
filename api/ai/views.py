from flask import Blueprint, request, jsonify
from .prediction_helper import get_prediction


ai_bp = Blueprint("ai", __name__, url_prefix="/model")


@ai_bp.route("/predict", methods=["POST"])
def predict():
    body = request.get_json()

    return jsonify({"prediction": get_prediction(body)[0]})

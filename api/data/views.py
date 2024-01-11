from flask import Blueprint
from .data_manager import check_data_status

import json

data_bp = Blueprint("data", __name__, url_prefix="/data")

@data_bp.route("/status", methods=["GET"])
def check_status():
  status = check_data_status()
  print(status)
  return json.dumps(status)

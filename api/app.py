"""Main app file"""
from flask import Flask
from flask_cors import CORS
from .ai.views import ai_bp
from .data.views import data_bp

def create_app():
  app = Flask(import_name=__name__)

  register_blueprints(app=app)
  init_cors(app=app)

  return app

def register_blueprints(app):
  app.register_blueprint(blueprint=ai_bp)
  app.register_blueprint(blueprint=data_bp)


def init_cors(app):
  CORS(app)

if __name__ == "__main__":
  main_app = create_app()
  main_app.run(debug=True)
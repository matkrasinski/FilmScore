"""Main app file"""
from flask import Flask
from .ai.views import ai_bp
from .data.views import data_bp

def create_app():
  app = Flask(import_name=__name__)

  register_blueprints(app=app)

  return app

def register_blueprints(app):
  app.register_blueprint(blueprint=ai_bp)
  app.register_blueprint(blueprint=data_bp)


if __name__ == "__main__":
  main_app = create_app()
  main_app.run(debug=True)
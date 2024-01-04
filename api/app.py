"""Main app file"""
from flask import Flask


def create_app():
  app = Flask(import_name=__name__)
  return app


if __name__ == "__main__":
  main_app = create_app()
  main_app.run(debug=True)
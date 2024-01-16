import pandas as pd
import os
from ...ai.preprocessing.preprocessor import *
from ...ai.model_loader import predict_rating

movies = []
new_movies = []


def get_all_movies():
  global movies, new_movies
  # if len(movies) == 0:
  #   movies = save_movies()
  #   movies = movies.to_dict(orient="records")

  if movies is None or len(movies) == 0:
    load_movies()

  if type(movies) == pd.DataFrame:
    movies = movies.to_dict(orient="records")
  return movies[:1000]

def find_released_movies(page, size):
  global movies
  if movies is None or len(movies) == 0:
    # print("Released Movies", len(movies))
    load_movies()

  if type(movies) == pd.DataFrame:
    movies = movies.to_dict(orient="records")

  # print(len(movies), type(movies))
  return movies[page * size: (page * size) + size]


def find_new_movies(page, size):
  global new_movies
  if new_movies is None or len(new_movies) == 0:
    # print("New Movies", len(new_movies))  
    load_movies()

  if "prediction" not in new_movies and type(new_movies) == pd.DataFrame:
    new_movies = split_people(new_movies)
    new_movies = adjust_data(new_movies)
    new_movies = apply_ratings(new_movies)
    new_movies = fillna(new_movies)
    new_movies.dropna(inplace=True)
    new_movies["prediction"] = predict_rating(new_movies)
    

  if type(new_movies) == pd.DataFrame:
    new_movies = new_movies.to_dict(orient="records")
  # print(len(new_movies), type(new_movies))
  return new_movies[page * size: (page * size) + size]

def load_movies():
  try:
    loaded = pd.read_csv("imdb/movies.csv")
    print(loaded.columns)
    # loaded = split_people(loaded)
    # loaded = adjust_data(loaded)
    loaded = fillna(loaded)
    
    split_movies(loaded)
  except:
    save_movies()
    load_movies()

    
def split_movies(all_movies):
  global movies, new_movies
  movies = all_movies[all_movies["status"] == "Released"]
  new_movies = all_movies[all_movies["status"] != "Released"]
  print("Released len: ", len(movies))
  print("New len: ", len(new_movies))


def save_movies():
  movies = merge_tmdb_imdb(how="left")
  movies = adjust_people(movies)
  
  movies.to_csv("imdb/movies.csv", index=False)
  return movies 

# get_all_movies()
# save_movies()
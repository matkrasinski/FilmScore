import pandas as pd
import os
from ...ai.preprocessing.preprocessor import merge_tmdb_imdb, adjust_data, adjust_people, fillna, split_people

movies = []

def get_all_movies():
  global movies
  # if len(movies) == 0:
  #   movies = save_movies()
  #   movies = movies.to_dict(orient="records")

  movies = load_movies()
  movies = movies.to_dict(orient="records")
  return movies[:1000]


def load_movies():
  try:
    loaded = pd.read_csv("imdb/movies.csv", nrows=1000)
    print(loaded.columns)
    loaded = split_people(loaded)
    loaded = adjust_data(loaded)
    return fillna(loaded)
  except:
    save_movies()
    load_movies()
    
  


def save_movies():
  movies = merge_tmdb_imdb()
  movies = adjust_people(movies)
  
  movies.to_csv("imdb/movies.csv", index=False)
  return movies 

# get_all_movies()
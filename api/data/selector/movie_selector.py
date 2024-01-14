import pandas as pd
import os
from ...ai.preprocessing.preprocessor import merge_tmdb_imdb, adjust_data, adjust_people, fillna, split_people

movies = []
new_movies = []


def get_all_movies():
  global movies, new_movies
  # if len(movies) == 0:
  #   movies = save_movies()
  #   movies = movies.to_dict(orient="records")

  movies = load_movies()
  movies = movies.to_dict(orient="records")
  return movies[:1000]

def find_released_movies(page, size):
  global movies
  if len(movies) == 0:
    print("Released Movies", len(movies))
    load_movies()

  if type(movies) == pd.DataFrame:
    movies = movies.to_dict(orient="records")

  print(len(movies), type(movies))
  return movies[page * size: (page * size) + size]


def find_new_movies(page, size):
  global new_movies
  if len(new_movies) == 0:
    print("New Movies", len(new_movies))  
    load_movies()
    new_movies = new_movies.to_dict(orient="records")

  if type(new_movies) == pd.DataFrame:
    new_movies = new_movies.to_dict(orient="records")
  print(len(new_movies), type(new_movies))
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
  movies = all_movies[all_movies["status"] == "Released"][all_movies["numVotes"] > 100]
  new_movies = all_movies[all_movies["status"] != "Released"][all_movies["numVotes"] <= 100]
  print("Released len: ", len(movies))
  print("New len: ", len(new_movies))


def save_movies():
  movies = merge_tmdb_imdb(how="left")
  movies = adjust_people(movies)
  
  movies.to_csv("imdb/movies.csv", index=False)
  return movies 

# get_all_movies()
# save_movies()
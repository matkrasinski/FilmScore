import pandas as pd

people = []

def retrieve_all_people():
  global people
  if len(people) == 0:
    people = pd.read_csv("imdb/name.basics.tsv", sep="\t", nrows=50000)
  return people.set_index("nconst")["primaryName"].to_dict()


def retrieve_genres():
  # tmdb_data = pd.read_csv("tmdb/tmdb.csv")
  # tmdb_data.dropna(inplace=True)
  # unique = set()
  # for _, row in tmdb_data.iterrows():
  #   genres = row["genres"].split("|")
  #   for genre in genres:
  #     unique.add(genre)
  # print(unique)
  # return list(unique)
  genres = ["Drama", "Adventure", "Mystery",
            "History", "Romance", "Horror",
            "Animation", "TV Movie", "Science Fiction",
            "Music", "Action", "Western", "Fantasy",
            "Crime", "Family", "War",
            "Thriller", "Documentary", "Comedy"]
  
  return genres


unique_companies = set()
unique_languages = set()

def retrieve_companies_languages():
  global unique_companies, unique_languages
  if len(unique_languages) == 0 or len(unique_companies) == 0:
    init()
  
  return list(unique_companies), list(unique_languages)
  

def init():
  tmdb_data = pd.read_csv("tmdb/tmdb.csv")
  tmdb_data.dropna(inplace=True)
  
  for _, row in tmdb_data.iterrows():
    genres = row["production_companies"].split("|")
    for genre in genres:
      unique_companies.add(genre)

    languages = row["spoken_languages"].split("|")
    for lang in languages:
      unique_languages.add(lang)
  # print(unique)
  # return list(unique)
import pandas as pd
import numpy as np

def prepare_tmdb_data():
  tmdb_data = pd.read_csv("tmdb/tmdb.csv")
  tmdb_data = tmdb_data.drop(columns=["budget", "production_countries", "vote_average", "vote_count", "cast", "crew"])
  tmdb_data = tmdb_data[tmdb_data["runtime"] != 0]
  tmdb_data.reset_index(drop=True)

  imdb_ratings = pd.read_csv("imdb/title.ratings.tsv", sep="\t")
  tmdb_data = tmdb_data.merge(imdb_ratings, left_on="imdb_id", right_on="tconst", how="inner")

  directors = prepare_directors()
  tmdb_data = tmdb_data.merge(directors, left_on="imdb_id", right_on="tconst", how="inner")

  actors = prepare_actors()
  tmdb_data = tmdb_data.merge(actors, left_on="imdb_id", right_on="tconst", how="inner")

  tmdb_data = tmdb_data[tmdb_data["release_date"] >= "1970-01-01"]
  tmdb_data = tmdb_data[tmdb_data["numVotes"] >= 100]
  tmdb_data = tmdb_data[tmdb_data["runtime"] >= 60]

  print("prepare_tmdb_data ", len(tmdb_data))

  return tmdb_data


def prepare_directors():
  directors_df = pd.read_csv("imdb/title.crew.tsv", sep="\t")
  directors_df = directors_df[["tconst", "directors"]]
  directors_df["directors"] = directors_df['directors'].apply(lambda x: [] if x == '\\N' else x.split(','))
  return directors_df

def prepare_actors():
  principals_df = pd.read_csv("imdb/title.principals.tsv", sep="\t")
  
  actors_df = principals_df[principals_df['category'].isin(["actor", "actress"])]
  actors_df = actors_df.groupby("tconst")["nconst"].agg(list).reset_index()
  actors_df.columns = ["tconst", "actors"]

  return actors_df


def apply_ratings(data):
  people_ratings = pd.read_csv("generated/people_ratings.csv")
  people_ratings = people_ratings.set_index("nconst")["value_column"].to_dict()
  data["directors_rating"] = data["directors"].apply(lambda x: np.mean([people_ratings[director] for director in x if director in people_ratings]))
  data["actors_rating"] = data["actors"].apply(lambda x: np.mean([people_ratings[actor] for actor in x if actor in people_ratings]))

  companies_ratings = pd.read_csv("generated/companies_ratings.csv")
  companies_ratings = companies_ratings.set_index("company")["rating"].to_dict()
  data["companies_rating"] = data["production_companies"].apply(lambda x: np.mean([companies_ratings[company] for company in x if company in companies_ratings]))
  print("apply_ratings  ", len(data))

  return data


def adjust_data(data):
  data["genres"] = data["genres"].str.split("|")
  # data["directors"] = data["directors"].str.split("|")
  # data["actors"] = data["actors"].str.split("|")
  data["production_companies"] = data["production_companies"].str.split("|")
  data["spoken_languages"] = data["spoken_languages"].str.split("|")

  # data["directors_rating"] = data["directors_rating"].fillna(0.596247)
  # data["actors_rating"] = data["actors_rating"].fillna(0.580406)
  # data["companies_rating"] = data["companies_rating"].fillna(0.572576)

  data["belongs_to_collection"] = data["belongs_to_collection"].fillna("").apply(lambda x: str(int(x)) if x != "" else "")
  # data['keywords'] = data['keywords'].apply(lambda d: d if isinstance(d, str) else '')
  data['keywords'] = data['keywords'].str.replace("|", " ")
  data['videos'] = data['videos'].apply(lambda d: d if isinstance(d, str) else '')

  data['production_companies'] = data['production_companies'].apply(lambda d: d if isinstance(d, list) else [])
  data['actors'] = data['actors'].apply(lambda d: d if isinstance(d, list) else [])
  data['directors'] = data['directors'].apply(lambda d: d if isinstance(d, list) else [])
  data['genres'] = data['genres'].apply(lambda d: d if isinstance(d, list) else [])
  data['spoken_languages'] = data['spoken_languages'].apply(lambda d: d if isinstance(d, list) else [])

  print("adjust_data ", len(data))
  return data



def fillna_ratings(data):
  data["directors_rating"].fillna(0.6, inplace=True)
  data["actors_rating"].fillna(0.6, inplace=True)
  data["companies_rating"].fillna(0.6, inplace=True)
  
  return data


def fillna(data):
  data["keywords"].fillna("", inplace=True)

  return fillna_ratings(data)



def prepare_data():
  tmdb_data = prepare_tmdb_data()
  tmdb_data = adjust_data(tmdb_data)
  tmdb_data = apply_ratings(tmdb_data)
  
  return fillna(tmdb_data)

  
import pandas as pd
import numpy as np
import os
from .companies_ratings import get_companies_ratings

columns = ["imdb_id", "id", "production_companies", "release_date", "runtime", "status"]

def normalize_feature(data):
    return (data - data.min()) / (data.max() - data.min())

def std_normalize_feature(data):
  x_std = (data - data.min()) / (data.max() - data.min())
  return x_std * (data.max() - data.min()) + data.min()


def generate_ratings():
  tmdb_data = pd.read_csv("tmdb/tmdb.csv")
  print("TMDB data loaded")
  tmdb_data = tmdb_data[columns]



  # tmdb_data["keywords"] = tmdb_data["keywords"].str.split("|")
  # tmdb_data["genres"] = tmdb_data["genres"].str.split("|")
  # df["crew"] = df["crew"].str.split("|")
  # df["cast"] = df["cast"].str.split("|")

  tmdb_data["production_companies"] = tmdb_data["production_companies"].str.split("|")
  # tmdb_data["spoken_languages"] = tmdb_data["spoken_languages"].str.split("|")

  tmdb_data["production_companies"] = tmdb_data["production_companies"].apply(lambda x: x if isinstance(x, list) else [])
  # tmdb_data["genres"] = tmdb_data["genres"].apply(lambda x: x if isinstance(x, list) else [])
  # tmdb_data["spoken_languages"] = tmdb_data["spoken_languages"].apply(lambda x: x if isinstance(x, list) else [])
  # tmdb_data["keywords"] = tmdb_data["keywords"].apply(lambda x: x if isinstance(x, list) else [])


  print("keywords, generes, production_companies and spoken_languages separated")

  tmdb_data = tmdb_data[tmdb_data["status"] == "Released"]#[["belongs_to_collection", "keywords", "genres", "original_language", "spoken_languages", "production_companies", "runtime", "release_date", "videos", "id", "imdb_id"]]
  # tmdb_data["keywords"] = tmdb_data["keywords"].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)

  print("Before filter ", len(tmdb_data))
  # tmdb_data = tmdb_data.dropna()
  # tmdb_data = tmdb_data.reset_index(drop=True)

  tmdb_data = tmdb_data[tmdb_data["release_date"] != '']

  imdb_ratings = pd.read_csv("imdb/title.ratings.tsv", sep="\t")
  print("IMDB ratings loaded")

  tmdb_data = tmdb_data.merge(imdb_ratings, left_on="imdb_id", right_on="tconst", how="inner")
  print("IMDB-TMDB data merged on ratings")

  tmdb_data = tmdb_data[tmdb_data["numVotes"] >= 100]
  tmdb_data = tmdb_data[tmdb_data["release_date"] >= "1970-01-01"]
  tmdb_data = tmdb_data[tmdb_data["runtime"] >= 60]
  print("After filter ", len(tmdb_data))

  directors_df = pd.read_csv("imdb/title.crew.tsv", sep="\t")
  directors_df = directors_df[["tconst", "directors"]]
  directors_df["directors"] = directors_df['directors'].apply(lambda x: [] if x == '\\N' else x.split(','))
  print("IMDB directors dataframe ready")

  tmdb_data = tmdb_data.merge(directors_df, left_on="imdb_id", right_on="tconst", how="inner")
  print("IMDB-TMDB data merged on directors")

  principals_df = pd.read_csv("imdb/title.principals.tsv", sep="\t")
  print("IMDB principals loaded")

  actors_df = principals_df[principals_df['category'].isin(["actor", "actress"])]
  actors_df = actors_df.groupby("tconst")["nconst"].agg(list).reset_index()
  actors_df.columns = ["tconst", "actors"]
  print("IMDB actors datafraem ready")

  tmdb_data = tmdb_data.merge(actors_df, left_on="imdb_id", right_on="tconst", how="inner")
  print("IMDB-TMDB data merged on actors")



  actor_weight=1
  movies_num_weight=0.15
  num_votes_weight=0.55

  categories = ["actress", "actor", "director"]

  principals_df = principals_df[principals_df["category"].isin(categories)]
  print("IMDB actors and directors only in principals")

  names = pd.read_csv("imdb/name.basics.tsv", sep='\t')
  print("IMDB names loaded")

  names_principals = names.merge(principals_df, on="nconst", how="right")
  names_principals_basics = names_principals.merge(imdb_ratings, on="tconst")
  print("IMDB names-principals merged")


  people_ratings = normalize_feature(names_principals_basics.groupby("nconst")["averageRating"].mean())
  number_of_movies = normalize_feature(names_principals_basics.groupby('nconst').size())
  num_votes = normalize_feature(names_principals_basics.groupby('nconst')['numVotes'].sum())

  people_ratings = (actor_weight * people_ratings) + (movies_num_weight * number_of_movies) + (num_votes_weight * num_votes)
  print("People ratings ready")
  data_directory = 'generated'
  if not os.path.exists(data_directory):
      os.mkdir(data_directory)

  people_ratings = pd.DataFrame({'nconst': people_ratings.index, 'rating': people_ratings.values})
  people_ratings.to_csv("generated/people_ratings.csv", index=False)

  companies_ratings = get_companies_ratings(tmdb_data)
  companies_ratings = pd.DataFrame(list(companies_ratings.items()), columns=['company', 'rating'])
  companies_ratings.to_csv("generated/companies_ratings.csv", index=False)
  print("Companies ratings ready")



  # tmdb_data["directors_rating"] = tmdb_data["directors"].apply(lambda x: np.mean([people_ratings[director] for director in x if director in people_ratings]))
  # tmdb_data["actors_rating"] = tmdb_data["actors"].apply(lambda x: np.mean([people_ratings[actor] for actor in x if actor in people_ratings]))
  # tmdb_data["companies_rating"] = tmdb_data["production_companies"].apply(lambda x: np.mean([companies_ratings[company] for company in x if company in companies_ratings]))

  # print("Before save")
  # tmdb_data.to_csv("ready_data.csv", index=False)
  print("Data saved!")
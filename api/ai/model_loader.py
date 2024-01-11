from joblib import dump, load
from .transformers import *
from .preprocessing.preprocessor import prepare_data, apply_ratings, fillna
from .model.knn import prepare_model
from ..data.status.status_checker import check_file_status
from ..data.status.file_status import FileStatus

# import pandas as pd

# model = load("model")

# new_data = pd.read_csv("prep_data.csv")


# new_data["genres"] = new_data["genres"].str.split("|")
# new_data["directors"] = new_data["directors"].str.split("|")
# new_data["actors"] = new_data["actors"].str.split("|")
# new_data["production_companies"] = new_data["production_companies"].str.split("|")
# new_data["spoken_languages"] = new_data["spoken_languages"].str.split("|")

# new_data["directors_rating"] = new_data["directors_rating"].fillna(0.596247)
# new_data["actors_rating"] = new_data["actors_rating"].fillna(0.580406)
# new_data["companies_rating"] = new_data["companies_rating"].fillna(0.572576)

# new_data["belongs_to_collection"] = new_data["belongs_to_collection"].fillna("").apply(lambda x: str(int(x)) if x != "" else "")
# new_data['keywords'] = new_data['keywords'].apply(lambda d: d if isinstance(d, str) else '')
# new_data['videos'] = new_data['videos'].apply(lambda d: d if isinstance(d, str) else '')

# new_data['production_companies'] = new_data['production_companies'].apply(lambda d: d if isinstance(d, list) else [])
# new_data['actors'] = new_data['actors'].apply(lambda d: d if isinstance(d, list) else [])
# new_data['directors'] = new_data['directors'].apply(lambda d: d if isinstance(d, list) else [])
# new_data['genres'] = new_data['genres'].apply(lambda d: d if isinstance(d, list) else [])
# new_data['spoken_languages'] = new_data['spoken_languages'].apply(lambda d: d if isinstance(d, list) else [])


# print(new_data.columns)



# predictions = model.predict(new_data)
# new_data["prediction"] = predictions
# new_data[["imdb_id", "original_title", "prediction", "release_date"]].sort_values(by="release_date", ascending=True).to_csv("predictions.csv", index=False)


# prep = model.named_steps.preprocessor
# print(new_data["videos"].str.cat())

# transformed = prep.transform(new_data)

# distances, indices = model.named_steps.knn.kneighbors(transformed)

# print(f"Closest neighbors indices: {indices.flatten()}")
# print(f"Distances to closest neighbors: {distances.flatten()}")

model = None

def load_model(generate=False, model_path="model.joblib"):
  global model
  model_status = check_file_status(model_path)
  if generate or model_status["status"] != FileStatus.OK:
    model = generate_model()
  else:
    model = load(model_path)

  return model


def generate_model(save=True):
  data = prepare_data()
  model = prepare_model()
  X_columns = ["belongs_to_collection", "keywords", "genres", "original_language",
              "spoken_languages", "production_companies", "actors", "directors",
              "runtime", "release_date", "videos", "actors_rating", "directors_rating",
              "companies_rating", "id", "imdb_id"]
  y_column = "averageRating"
  data.to_csv("wtf_data.csv", index=False)
  print(data.iloc[0])

  model.fit(data[X_columns], data[y_column])

  if save:
    dump(model, "model.joblib")

  return


def predict_rating(data):
  global model
  data = apply_ratings(data)
  data = fillna(data)
  print(data)
  if model is None:
    model = load_model() 
  print(data)
  result = model.predict(data)
  print(result)
  return result[0]
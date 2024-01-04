from joblib import load
from transformers import *

import pandas as pd

model = load("model")

new_data = pd.read_csv("new_data.csv")
print(new_data)


new_data["genres"] = new_data["genres"].str.split("|")
new_data["directors"] = new_data["directors"].str.split("|")
new_data["actors"] = new_data["actors"].str.split("|")
new_data["production_companies"] = new_data["production_companies"].str.split("|")
new_data["spoken_languages"] = new_data["spoken_languages"].str.split("|")

print(model.predict(new_data))
prep = model.named_steps.preprocessor
# print(new_data["videos"].str.cat())

# transformed = prep.transform(new_data)

# distances, indices = model.named_steps.knn.kneighbors(transformed)

# print(f"Closest neighbors indices: {indices.flatten()}")
# print(f"Distances to closest neighbors: {distances.flatten()}")
import pandas as pd

companies_ratings = {}
actor_weight=1
movies_num_weight=0.15
num_votes_weight=0.55

first_set = set()
second_set = set()
third_set = set()

# X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
# X_scaled = X_std * (max - min) + min
def std_normalize_feature(value, min, max):
  x_std = (value - min) / (max - min)
  return x_std * (max - min) + min

def normalize_feature(value, min, max):
  return (value - min) / (max - min)
  
def get_companies_ratings(data):
  for _, row in data.iterrows():
    for company in row["production_companies"]:
      if company in companies_ratings:
        companies_ratings[company][0] += row["averageRating"]
        companies_ratings[company][1] += row["numVotes"]
        companies_ratings[company][2] += 1
      else:
        companies_ratings[company] = [row["averageRating"], row["numVotes"], 1]

  for company in companies_ratings:
    companies_ratings[company][0] = companies_ratings[company][0] / companies_ratings[company][2]
    first_set.add(companies_ratings[company][0])
    third_set.add(companies_ratings[company][1])
    second_set.add(companies_ratings[company][2])

  first = (min(first_set), max(first_set))
  second = (min(second_set), max(second_set))
  third = (min(third_set), max(third_set))

  for company in companies_ratings:
    companies_ratings[company][0] = normalize_feature(companies_ratings[company][0], first[0], first[1])
    companies_ratings[company][1] = normalize_feature(companies_ratings[company][1], third[0], third[1])
    companies_ratings[company][2] = normalize_feature(companies_ratings[company][2], second[0], second[1])

  for company in companies_ratings:
    companies_ratings[company] = (companies_ratings[company][0] * actor_weight) + (companies_ratings[company][2] * movies_num_weight) + (companies_ratings[company][1] * num_votes_weight)


  return companies_ratings
  # min_rating = min(people_ratings.values())
  # max_rating = max(people_ratings.values())

  # print(min_rating)

  # for person in people_ratings:
  #   people_ratings[person] = (people_ratings[person] - min_rating) / (max_rating - min_rating)

  # companies_ratings_df = pd.DataFrame(list(companies_ratings.items()), columns=['company', 'rating'])
  # companies_ratings_df.columns = ["company", "rating"]

  # companies_ratings_df = companies_ratings_df.merge(names, left_on="company", right_on="nconst", how="inner")[["company", "primaryName", "rating"]]

  # companies_ratings_df.sort_values(by="rating", ascending=False).to_csv("companies.csv", index=False)

  # print(directors_ratings) 
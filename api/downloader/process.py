import pandas as pd


# names = pd.read_csv("imdb/name.basics.tsv", sep='\t')
# principals = pd.read_csv("imdb/title.principals.tsv", sep="\t")
# ratings = pd.read_csv("imdb/title.ratings.tsv", sep="\t")
movies = pd.read_csv("imdb/title.basics.tsv", sep="\t")
movies = movies[movies["startYear"] != '\\N']
movies = movies[movies["titleType"].isin(["movie", "tvMovie"])]

movies[movies["startYear"] >= '2024'].to_csv("new_releases.csv", index=False)

# categories = ["actress", "actor", "director"]

# current_principals_df = principals[principals["category"].isin(categories)]

# names_principals = names.merge(current_principals_df, on="nconst", how="right")
# names_principals_basics = names_principals.merge(ratings, on="tconst")

# def normalize_feature(data):
#     return (data - data.min()) / (data.max() - data.min())

# def std_normalize_feature(data):
#   x_std = (data - data.min()) / (data.max() - data.min())
#   return x_std * (data.max() - data.min()) + data.min()

# actor_weight=1
# movies_num_weight=0.15
# num_votes_weight=0.55

# actor_ratings = normalize_feature(names_principals_basics.groupby("nconst")["averageRating"].mean())
# number_of_movies = normalize_feature(names_principals_basics.groupby('nconst').size())
# num_votes = normalize_feature(names_principals_basics.groupby('nconst')['numVotes'].sum())

# actor_ratings = (actor_weight * actor_ratings) + (movies_num_weight * number_of_movies) + (num_votes_weight * num_votes)

# actor_ratings.sort_values(ascending=False).to_csv("people_ratings.csv")
# actor_ratings.hist()
# actor_ratings = normalize_feature(actor_ratings)

X_TRAIN_COLUMNS = ["belongs_to_collection", "keywords", "genres", "original_language",
                   "spoken_languages", "production_companies", "actors", "directors",
                   "runtime", "release_date", "videos", "actors_rating", "directors_rating",
                   "companies_rating", "id", "imdb_id"]

Y_TRAIN_COLUMN = "averageRating"

EXPORT_COLUMNS = ['id', 'imdb_id', 'original_title', 'genres', 'average_rating',
                  'predicted_rating', 'num_votes', 'keywords', 'belongs_to_collection',
                  'videos', 'runtime', 'original_language', 'spoken_languages', 'status',
                  'release_date', 'poster_source', 'production_companies', "actors", "directors"]


RUNTIME_COLUMN = "runtime"
BUDGET_COLUMN = "budget"
NUM_VOTES_IMDB_COLUMN = "numVotes"
NUM_VOTES_TMDB_COLUMN = "num_votes"
GENRES_COLUMN = "genres"
PRODUCTION_COMPANIES_COLUMN = "production_companies"

SPOKEN_LANGUAGES_COLUMN = "spoken_languages"
COLLECTION_COLUMN = "belongs_to_collection"
KEYWORDS_COLUMN = "keywords"
VIDEOS_COLUMN = "videos"
ACTORS_COLUMN = "actors"
DIRECTORS_COLUMN = "directors"
ACTORS_RATING_COLUMN = "actors_rating"
DIRECTORS_RATING_COLUMN = "directors_rating"
COMPANIES_RATING_COLUMN = "companies_rating"
TCONST_COLUMN = "tconst"
AVERAGE_RATING_IMDB_COLUMN = "averageRating"
AVERAGE_RATING_TMDB_COLUMN = "average_rating"
IMDB_ID_COLUMN = "imdb_id"
TMDB_ID_TMDB_COLUMN = "id"
TMDB_ID_COLUMN = "tmdb_id"
PREDICTED_RATING_COLUMN = "predicted_rating"
ORIGINAL_LANGUAGE_COLUMN = "original_language"
ORIGINAL_TITLE_COLUMN = "original_title"
POSTER_SOURCE_COLUMN = "poster_source"
STATUS_COLUMN = "status"
RELEASE_DATE_COLUMN = "release_date"

IMAGE_ID_NAME = "id"
IMAGE_PATH_COLUMN = "path"

COMPANY_ID_COLUMN = "company_id"
COMPANY_NAME_COLUMN = "company_name"
PERSON_ID_COLUMN = "person_id"
MOVIE_ID_COLUMN = "movie_id"
COLLECTION_ID_COLUMN = "collection_id"
CATEGORY_COLUMN = "category"
ACTOR_COLUMN = "actor"
DIRECTOR_COLUMN = "director"
RESULTS_COLUMN = "results"

ACTOR = "actor"
ACTRESS = "actress"
DIRECTOR = "director"

PRIMARY_NAME_IMDB_COLUMN = "primaryName"
PRIMARY_NAME_TMDB_COLUMN = "primary_name"
PERSON_COLUMN = "person"
COMPANY_COLUMN = "company"
RATING_COLUMN = "rating"

NCONST_COLUMN = "nconst"

ID = "id"
NAME = "name"

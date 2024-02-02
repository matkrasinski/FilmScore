import os
import pathlib

import pymysql

APP_NAME: str = "FilmScore"
DEBUG: bool = True
TESTING: bool = True


SQLALCHEMY_DATABASE_URI: str = "sqlite://///" + os.path.join(
    pathlib.Path(
        __file__).parent.parent, "sample_data/sqlite.db"
)
print(SQLALCHEMY_DATABASE_URI)

# pymysql.install_as_MySQLdb()
# SQLALCHEMY_DATABASE_URI: str = 'mysql://root:123123123123123123123@localhost:3306/FilmScoreDB'
TMDB_ACCESS_TOKEN: str = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzYWZhZWU3NjU2NDZlZTY1MWI3ZThlMzJiOTgwNjAyZCIsInN1YiI6IjY1NTBkNjAzZDRmZTA0MDExYjhmMWMxMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.l7kJ9dey1H6V3dkt30WvFxuEzA3qapjYC2n6RwBxye8"
GOOGLE_DRIVE_TMDB_DATA_URL: str = "https://drive.google.com/file/d/1KB04N6WcEKZ2DIZsxeX9IuqwsySaIOqg/view?usp=sharing"
IMDB_DATASET_URL: str = "https://datasets.imdbws.com/"
TMDB_EXPORTS_URL: str = "http://files.tmdb.org/p/exports/"
TMDB_API: str = "https://api.themoviedb.org/3/"

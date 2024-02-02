import pandas as pd

from ...data.downloader import downloader
from ...data.status import status_checker
from .FILES_NAMES import *

TITLE_BASICS = TITLE_BASIC_LOCAL_PATH if status_checker.check_creation_time_is_today(
    TITLE_BASIC_LOCAL_PATH) else downloader.download_IMDb_file(TITLE_BASIC_NAME)


def limit_principals(principals_path):
    title_basics = pd.read_csv(TITLE_BASICS, sep="\t")
    title_basics = title_basics[title_basics["titleType"].isin(
        ["movie", "tvMovie"])]
    ids = title_basics["tconst"].unique()
    principals = pd.read_csv(principals_path, sep="\t")
    principals = principals[principals["tconst"].isin(ids)]
    principals.to_csv(principals_path, index=False, sep="\t")

    return principals_path


TITLE_RATINGS = TITLE_RATINGS_LOCAL_PATH if status_checker.check_creation_time_is_today(
    TITLE_RATINGS_LOCAL_PATH) else downloader.download_IMDb_file(TITLE_RATINGS_NAME)
TITLE_PRINCIPALS = TITLE_PRINCIPALS_LOCAL_PATH if status_checker.check_creation_time_is_today(
    TITLE_PRINCIPALS_LOCAL_PATH) else limit_principals(downloader.download_IMDb_file(TITLE_PRINCIPALS_NAME))
TITLE_CREW = TITLE_CREW_LOCAL_PATH if status_checker.check_creation_time_is_today(
    TITLE_CREW_LOCAL_PATH) else downloader.download_IMDb_file(TITLE_CREW_NAME)
NAMES_BASICS = NAMES_BASICS_LOCAL_PATH if status_checker.check_creation_time_is_today(
    NAMES_BASICS_LOCAL_PATH) else downloader.download_IMDb_file(NAMES_BASICS_NAME)

TMDB_DATA = downloader.download_TMDB_data()
TMDB_MOVIES_IDS = downloader.download_TMDB_ids()
TMDB_COLLECTIONS = downloader.download_TMDB_ids(
    middle_name=TMDB_COLLECTIONS_IDS_NAME)
TMDB_COMPANIES_IDS = downloader.download_TMDB_ids(
    middle_name=TMDB_PRODUCTION_IDS_NAME)

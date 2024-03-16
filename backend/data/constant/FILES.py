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
    chunk_size = 200000
    filtered_chunks = []

    for chunk in pd.read_csv(principals_path, sep="\t", chunksize=chunk_size):
        filtered_chunk = chunk[chunk["tconst"].isin(ids)]
        filtered_chunks.append(filtered_chunk)

    principals = pd.concat(filtered_chunks, ignore_index=True)
    principals.to_csv(principals_path, index=False, sep="\t")

    return principals_path


TITLE_RATINGS = TITLE_RATINGS_LOCAL_PATH if status_checker.check_creation_time_is_today(
    TITLE_RATINGS_LOCAL_PATH) else downloader.download_IMDb_file(TITLE_RATINGS_NAME)
TITLE_PRINCIPALS = limit_principals(TITLE_PRINCIPALS_LOCAL_PATH) if status_checker.check_creation_time_is_today(
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

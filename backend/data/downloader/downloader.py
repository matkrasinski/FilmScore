import gzip
import os
from datetime import datetime

import gdown
import requests

from ..util.date_helper import get_post_update_date
from ...data.constant.FILES_NAMES import *
from ...settings import GOOGLE_DRIVE_TMDB_DATA_URL, TMDB_EXPORTS_URL, IMDB_DATASET_URL


file_names = [
    TITLE_PRINCIPALS_NAME,
    NAMES_BASICS_NAME,
    TITLE_RATINGS_NAME,
    TITLE_BASIC_NAME,
    TITLE_CREW_NAME
]


def download_file(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully to {destination}")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


def unzip_gz_file(gz_file_path, output_file_path):
    with gzip.open(gz_file_path, 'rb') as gz_file:
        with open(output_file_path, 'wb') as output_file:
            output_file.write(gz_file.read())
    print(f"File {gz_file_path} successfully unzipped to {output_file_path}")


def download_IMDb_files(data_directory=IMDB_LOCAL_DIR):
    if not os.path.exists(data_directory):
        os.mkdir(data_directory)
    for name in file_names:
        download_IMDb_file(name)


def download_IMDb_file(name, data_directory=IMDB_LOCAL_DIR):
    if not os.path.exists(data_directory):
        os.mkdir(data_directory)
    url = f'{IMDB_DATASET_URL}{name}.gz'
    download_file_destination = f'{data_directory}{name}.gz'

    download_file(url=url, destination=download_file_destination)
    unzip_gz_file(download_file_destination, f'{data_directory}{name}')
    if os.path.exists(download_file_destination):
        os.remove(download_file_destination)

    return f'{data_directory}{name}'


def download_TMDB_data(destination=TMDB_LOCAL_DIR, filename=TMDB_DATA_NAME):
    if not os.path.exists(destination):
        os.mkdir(destination)
    path = f'{destination}{filename}'

    if not os.path.exists(path):
        gdown.download(GOOGLE_DRIVE_TMDB_DATA_URL,
                       path, quiet=False, fuzzy=True)
    return path


def download_TMDB_ids(date=datetime.now(), destination=TMDB_LOCAL_DIR, middle_name=TMDB_MOVIE_IDS_NAME):
    formatted_date = get_post_update_date(date=date)
    formatted_date = formatted_date.strftime(
        "%m") + "_" + formatted_date.strftime("%d") + "_" + formatted_date.strftime("%G")
    file_name = f'{middle_name}_{formatted_date}.json'

    url = f'{TMDB_EXPORTS_URL}{file_name}.gz'
    downloaded_file_path = f'{destination}{file_name}.json.gz'

    if not os.path.exists(f'{destination}/{file_name}'):
        delete_movies_starting_with(destination, middle_name + "_")
        download_file(url, downloaded_file_path)
        unzip_gz_file(downloaded_file_path, f'{destination}{file_name}')
        if os.path.exists(downloaded_file_path):
            os.remove(downloaded_file_path)

    return f'{destination}{file_name}'


def delete_movies_starting_with(directory, prefix):
    for file in os.listdir(directory):
        if file.startswith(prefix):
            path = os.path.join(directory, file)
            os.remove(path)
            print(f'File deleted: {path}')

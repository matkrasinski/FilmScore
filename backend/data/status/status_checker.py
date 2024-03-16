import datetime
import os

from ..util.date_helper import date_from_today
from ...data.constant.FILES_NAMES import *
from .file_status import FileStatus
from ...data.constant.STATUSES import FS_STATUS_NAME, FS_CREATION_TIME

files = [
    NAMES_BASICS_LOCAL_PATH,
    TITLE_BASIC_LOCAL_PATH,
    TITLE_CREW_LOCAL_PATH,
    TITLE_PRINCIPALS_LOCAL_PATH,
    TITLE_RATINGS_LOCAL_PATH,

    TMDB_DATA_LOCAL_PATH,

    PEOPLE_RATINGS_LOCAL_PATH,
    COMPANIES_RATINGS_LOCAL_PATH
]


def check_files(files=files):
    info = {}
    for file in files:
        info[file] = check_file_status(file=file)
    return info


def check_file_status(file):
    file_info = {}
    if os.path.exists(file):
        creation_time_formatted = datetime.datetime.fromtimestamp(
            os.path.getctime(file))
        file_info[FS_STATUS_NAME] = FileStatus.OK
        file_info[FS_CREATION_TIME] = f'{creation_time_formatted}'
    else:
        file_info[FS_STATUS_NAME] = FileStatus.NOT_FOUND
        file_info[file] = f'File does not exist'
    return file_info


def check_IMDB_files():
    imdb_files = [file for file in files if file.startswith(IMDB_LOCAL_DIR)]
    return check_files(files=imdb_files)


def all_IMDB_files_exist():
    statuses = check_IMDB_files()
    return all(status[FS_STATUS_NAME] == FileStatus.OK for status in statuses.values())


def check_TMDB_files():
    tmdb_files = [file for file in files if file.startswith(TMDB_LOCAL_DIR)]
    return check_files(files=tmdb_files)


def all_TMDB_files_exist():
    statuses = check_TMDB_files()
    return all(status[FS_STATUS_NAME] == FileStatus.OK for status in statuses.values())


def check_ratings():
    ratings_files = [file for file in files if "ratings" in file]
    return check_files(files=ratings_files)


def all_ratings_generated():
    statuses = check_ratings()
    return all(status[FS_STATUS_NAME] == FileStatus.OK for status in statuses.values())


def check_all_files_exist():
    return all(status[FS_STATUS_NAME] == FileStatus.OK for status in check_files())


def check_creation_time_is_today(file_path):
    status = check_file_status(file_path)

    if status[FS_STATUS_NAME] != FileStatus.OK:
        return False
    return date_from_today(status[FS_CREATION_TIME])


def check_status():
    return check_files()

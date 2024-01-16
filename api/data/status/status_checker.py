import os
import datetime
from .file_status import FileStatus

files = [
  "imdb/name.basics.tsv",
  "imdb/title.basics.tsv",
  "imdb/title.crew.tsv",
  "imdb/title.principals.tsv",
  "imdb/title.ratings.tsv",

  "tmdb/tmdb_data.csv",

  "generated/companies_ratings.csv",
  "generated/people_ratings.csv",
]

def check_files(files=files):
  info = {}
  for file in files:
    info[file] = check_file_status(file=file)
  return info


def check_file_status(file):
  file_info = {}
  if os.path.exists(file):
    creation_time_formatted = datetime.datetime.fromtimestamp(os.path.getctime(file))
    file_info["status"] = FileStatus.OK
    file_info["creation_time"] = f'{creation_time_formatted}'
  else:
    file_info["status"] = FileStatus.NOT_FOUND
    file_info[file] = f'File does not exist'
  return file_info


def check_IMDB_files():
  imdb_files = [file for file in files if file.startswith("imdb/")]
  return check_files(files=imdb_files)


def all_IMDB_files_exist():
  statuses = check_IMDB_files()
  return all(status["status"] == FileStatus.OK for status in statuses.values())


def check_TMDB_files():
  tmdb_files = [file for file in files if file.startswith("tmdb/")]
  return check_files(files=tmdb_files)


def all_TMDB_files_exist():
  statuses = check_TMDB_files()
  return all(status["status"] == FileStatus.OK for status in statuses.values())


def check_ratings():
  ratings_files = [file for file in files if "ratings" in file]
  return check_files(files=ratings_files)


def all_ratings_generated():
  statuses = check_ratings()
  return all(status["status"] == FileStatus.OK for status in statuses.values())
  
def check_all_files_exist():
  return all(status["status"] == FileStatus.OK for status in check_files())


def check_status():
  return check_files()

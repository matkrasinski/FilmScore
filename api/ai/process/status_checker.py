import os
import datetime
from api.ai.process.file_status import FileStatus

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

def check_files(files=[]):
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

def all_IMDB_files_exist():
  imdb_files = [file for file in files if file.startswith("imdb/")]
  statuses = check_files(files=imdb_files)
  return all(status["status"] == FileStatus.OK for status in statuses.values())


def all_TMDB_files_exist():
  tmdb_files = [file for file in files if file.startswith("tmdb/")]
  statuses = check_files(files=tmdb_files)
  return all(status["status"] == FileStatus.OK for status in statuses.values())


def all_ratings_generated():
  ratings_files = [file for file in files if "ratings" in file]
  statuses = check_files(files=ratings_files)
  return all(status["status"] == FileStatus.OK for status in statuses.values())
  

def get_status():
  # print(check_files(files=files))
  print(all_IMDB_files_exist())

# get_status()
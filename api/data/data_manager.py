# from api.ai.process.status_checker import all_IMDB_files_exist, all_TMDB_files_exist, all_ratings_generated
# from api.ai.preprocessing.ratings_prep import generate_ratings

# from api.downloader.downloader import download_IMDB_files, download_TMDB_files
from .downloader.downloader import download_IMDB_files, download_TMDB_files
from .status.status_checker import *
from .generator.ratings_generator import generate_ratings



def download_all_IMDB_files(force=False):
  if not all_IMDB_files_exist() or force:
    download_IMDB_files()
  return check_IMDB_files()

def download_all_TMDB_files(force=False):
  if not all_TMDB_files_exist() or force:
    download_TMDB_files()
  return check_TMDB_files()

def generate_all_ratings(force=False):
  if (not all_ratings_generated() or force) and (all_TMDB_files_exist() and all_IMDB_files_exist()):
    generate_ratings()
  return check_ratings()

def check_data_status():
  return check_status()

# TODO
def update_data():
  return




# download_all_IMDB_files()
# download_all_TMDB_files()
# generate_all_ratings(force=True)


from api.ai.process.status_checker import check_IMDB_files
from api.ai.preprocessing.ratings_prep import generate_ratings

from api.downloader.downloader import download_IMDB_files, download_TMDB_files


def download_all_IMDB_files(force=False):
  if not all_IMDB_files_exist() or force:
    download_IMDB_files()
  return

def download_all_TMDB_files(force=False):
  if not all_TMDB_files_exist() or force:
    download_TMDB_files()
  return

def generate_all_ratings(force=False):
  if not all_ratings_generated() or force:
    generate_ratings()
  return check_IMDB_files()


# download_all_IMDB_files()
# download_all_TMDB_files()
generate_all_ratings(force=True)



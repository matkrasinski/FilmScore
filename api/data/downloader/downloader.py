import requests
import gzip
import os
import gdown

file_names = [
  "title.principals.tsv",
  "name.basics.tsv",
  "title.ratings.tsv",
  "title.basics.tsv",
  "title.crew.tsv"
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


# Example usage:
# url = 'https://files.tmdb.org/p/exports/movie_ids_12_17_2023.json.gz'
def download_IMDB_files():
    data_directory = 'imdb'
    if not os.path.exists(data_directory):
        os.mkdir(data_directory)

    # urls = [f'https://datasets.imdbws.com/{name}.gz' for name in file_names]

    # print(urls)

    for name in file_names:
        url = f'https://datasets.imdbws.com/{name}.gz'
        download_file_destination = f'{data_directory}/{name}.gz'
        
        download_file(url=url, destination=download_file_destination)
        unzip_gz_file(download_file_destination, f'{data_directory}/{name}')
        if os.path.exists(download_file_destination):
            os.remove(download_file_destination)

def download_TMDB_files():
    data_directory = 'tmdb'
    if not os.path.exists(data_directory):
        os.mkdir(data_directory)

    # urls = [f'https://datasets.imdbws.com/{name}.gz' for name in file_names]

    # print(urls)


    gdown.download("https://drive.google.com/file/d/1KB04N6WcEKZ2DIZsxeX9IuqwsySaIOqg/view?usp=drive_link", "tmdb/tmdb.csv", quiet=False, fuzzy=True)

    # for name in file_names:
    #     url = f'https://datasets.imdbws.com/{name}.gz'
    #     download_file_destination = f'{data_directory}/{name}.gz'
        
    #     download_file(url=url, destination=download_file_destination)
    #     unzip_gz_file(download_file_destination, f'{data_directory}/{name}')
    #     if os.path.exists(download_file_destination):
    #         os.remove(download_file_destination)


# url = 'https://datasets.imdbws.com/title.principals.tsv.gz'
# destination = 'imdb/title.principals.tsv.gz'
# file_destination = 'imdb/title.principals.tsv'

# download_file(url, destination)
# unzip_gz_file(destination, file_destination)


# download_IMDB_files()
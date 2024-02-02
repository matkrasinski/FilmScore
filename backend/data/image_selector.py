import requests
import pandas as pd
import os
from lxml import html
from .constant.FILES_NAMES import *
from .constant.COLUMNS import IMAGE_ID_NAME, IMAGE_PATH_COLUMN


def find_image(id, save=False, only_local=False):
    attempt = find_in_saved(id)
    if attempt is not None:
        return attempt

    if only_local:
        return

    return find_by_xpath(id, save=save)


def find_by_xpath(id, save=True):

    url = f'{TMDB_MOVIE_URL}{id}'
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    html_content = response.content

    tree = html.fromstring(html_content)

    xpath_expression = '//*[@id="original_header"]/div[1]/div[1]/div[1]/div/img/@src'
    image_url = tree.xpath(xpath_expression)
    if len(image_url) == 0:
        return

    image = image_url[0].split("/")[-1]
    image_path = f'{TMDB_POSTER_URL}{image}'

    if save:
        save_to_csv(id, image_path)

    return image_path


def find_in_saved(id):
    if not os.path.exists(TMDB_IMAGES_LOCAL_PATH):
        return None

    id_str = str(id)
    image_paths = pd.read_csv(TMDB_IMAGES_LOCAL_PATH, dtype=str)

    if id_str in image_paths[IMAGE_ID_NAME].values:
        return image_paths.loc[image_paths[IMAGE_ID_NAME] == id_str, IMAGE_PATH_COLUMN].iloc[0]

    return None


def save_to_csv(new_id, new_path):
    if not os.path.exists(TMDB_IMAGES_LOCAL_PATH):
        new_record = {IMAGE_ID_NAME: new_id, IMAGE_PATH_COLUMN: new_path}
        new_df = pd.DataFrame([new_record])
        new_df.to_csv(TMDB_IMAGES_LOCAL_PATH, index=False)
        return

    existing_paths = pd.read_csv(TMDB_IMAGES_LOCAL_PATH)

    existing_paths[IMAGE_ID_NAME] = existing_paths[IMAGE_ID_NAME].astype(str)
    new_id = str(new_id)

    if new_id in existing_paths[IMAGE_ID_NAME].values:
        pass
    else:
        new_record = {IMAGE_ID_NAME: new_id, IMAGE_PATH_COLUMN: new_path}
        existing_paths = pd.concat(
            [existing_paths, pd.DataFrame([new_record])], ignore_index=True)

    existing_paths.to_csv(TMDB_IMAGES_LOCAL_PATH, index=False)

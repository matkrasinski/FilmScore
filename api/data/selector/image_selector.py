import requests
import pandas as pd
import os
from lxml import html

def find_image(id):
    attempt = find_in_saved(id)
    if attempt is not None:
        print("LOADED IMAGE PATH FROM FILE")
        print(attempt)
        return attempt

    return find_by_xpath(id)


def find_by_xpath(id):
    url = f'https://www.themoviedb.org/movie/{id}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    html_content = response.content
    tree = html.fromstring(html_content)

    xpath_expression = '/html/body/div[1]/main/section/div[2]/div/div/section/div[1]/div[1]/div[1]/img/@src'
    image_url = tree.xpath(xpath_expression)
    if not image_url:
        print('Nie znaleziono URL do zdjęcia na stronie.')
        return
    print(f'URL do pierwszego zdjęcia: {image_url[0]}')
    image = image_url[0].split("/")[-1]
    image_path = f'https://image.tmdb.org/t/p/w300/{image}'

    save_to_csv(id, image_path)
    return image_path


def find_in_saved(id):
    if not os.path.exists("generated/imagePaths.csv"):
        return None

    id_str = str(id)
    image_paths = pd.read_csv("generated/imagePaths.csv", dtype=str)

    if id_str in image_paths['id'].values:
        return image_paths.loc[image_paths['id'] == id_str, 'path'].iloc[0]

    return None


def save_to_csv(new_id, new_path):
    csv_file = "generated/imagePaths.csv"

    if not os.path.exists(csv_file):
        new_record = {"id": new_id, "path": new_path}
        new_df = pd.DataFrame([new_record])
        new_df.to_csv(csv_file, index=False)
        print("CREATED IMAGE PATHS FILE")
        return

    existing_paths = pd.read_csv(csv_file)

    # Convert 'id' column to string to ensure proper comparison
    existing_paths['id'] = existing_paths['id'].astype(str)
    new_id = str(new_id)

    if new_id in existing_paths['id'].values:
        # Update existing record
        existing_paths.loc[existing_paths['id'] == new_id, 'path'] = new_path
    else:
        # Add new record
        new_record = {"id": new_id, "path": new_path}
        existing_paths = pd.concat([existing_paths, pd.DataFrame([new_record])], ignore_index=True)

    existing_paths.to_csv(csv_file, index=False)
    print("UPDATED IMAGE PATHS FILE")



# Przykład użycia
# id_to_search = "123456"
# result_path = find_image(id_to_search)
# print(f"Final Image Path: {result_path}")

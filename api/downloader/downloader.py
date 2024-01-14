import requests
from lxml import html

# Podaj URL strony
url = 'https://www.themoviedb.org/tv/202411-monarch-legacy-of-monsters'

# Pobierz zawartość strony
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
response = requests.get(url, headers=headers)

html_content = response.content
print(response)
# Zainicjuj obiekt drzewa HTML przy użyciu lxml
tree = html.fromstring(html_content)

# Znajdź pierwsze zdjęcie za pomocą ścieżki XPath
xpath_expression = '/html/body/div[1]/main/section/div[2]/div/div/section/div[1]/div[1]/div[1]/img/@src'  # Tutaj podaj odpowiednią ścieżkę XPath
image_url = tree.xpath(xpath_expression)

# Sprawdź czy znaleziono URL do zdjęcia
if image_url:
    print(f'URL do pierwszego zdjęcia: {image_url[0]}')
else:
    print('Nie znaleziono URL do zdjęcia na stronie.')

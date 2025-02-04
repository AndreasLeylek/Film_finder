import requests
from bs4 import BeautifulSoup
from TMDB import get_imdb_id_from_tmdb  # Importiere nur das, was du brauchst

def scrape_imdb_description(imdb_id, language="de"):
    """Scrapt die IMDb-Beschreibung basierend auf der IMDb-ID."""
    url = f"https://www.imdb.de/title/{imdb_id}/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": language
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Suche nach dem Tag, der die Plotbeschreibung enthält
        description_tag = soup.find('span', {'data-testid': 'plot-xl'})

        if description_tag:
            description = description_tag.text.strip()
        else:
            description = "Keine Beschreibung gefunden"

        return description
    else:
        print(f"Fehler beim Abrufen der IMDb-Seite: {response.status_code}")
        return None


def scrape_multiple_movie_descriptions(movies):
    """Scrape IMDb-Beschreibungen für eine Liste von Filmen basierend auf deren TMDb-IDs."""

    for movie in movies:
        tmdb_movie_id = movie.get('id')  # TMDb-ID des Films
        title = movie.get('title')  # Titel des Films

        # IMDb-ID basierend auf der TMDb-ID holen
        imdb_id = get_imdb_id_from_tmdb(tmdb_movie_id)

        if imdb_id:
            # Scrape IMDb-Beschreibung basierend auf der IMDb-ID
            description = scrape_imdb_description(imdb_id)
            print(f"Film: {title}\nIMDb-ID: {imdb_id}\nBeschreibung: {description}\n")
        else:
            print(f"IMDb-ID für den Film {title} nicht gefunden.")


import requests
import random
from API_KEY_URL import BEARER_TOKEN, url, HEADERS

#test abfrage, ob ich von der API einen Film mit der ID 550 bekomme (550 = The Matrix)
# Funktion zum Testen der TMDb-Verbindung
# def test_tmdb_connection():
#     response = requests.get(f"{url}/movie/550", headers=HEADERS)
#     if response.status_code == 200:
#         print("Verbindung erfolgreich! Token funktioniert endlich.")
#     elif response.status_code == 401:
#         print("Fehler: 401 - ich hasse dich.")
#     else:
#         print(f"Fehler: {response.status_code}")

# # Testen der Verbindung beim Start des Programms
# test_tmdb_connection()

# Hilfsfunktion für API-Anfragen
def make_request(request_url, params=None):
    response = requests.get(request_url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler bei der API-Abfrage: {response.status_code}")
        return None

# Funktion zum Abrufen der IMDb-ID basierend auf der TMDb-ID
def get_imdb_id_from_tmdb(tmdb_movie_id):
    movie_url = f"{url}/movie/{tmdb_movie_id}"
    movie_data = make_request(movie_url)
    if movie_data:
        return movie_data.get("imdb_id")
    print("Keine IMDb-ID gefunden.")
    return None

# Funktion zur Ermittlung des Laufzeitbereichs basierend auf dem Slider-Wert
def get_runtime_range(slider_value):
    ranges = {
        1: (0, 60),       # 0 bis 1 Stunde
        2: (61, 120),     # 1 bis 2 Stunden
        3: (121, 180),    # 2 bis 3 Stunden
        4: (181, 600)     # 3+ Stunden
    }
    return ranges.get(slider_value, (0, 600))

# Funktion zur Erstellung der Basisparameter für die API-Anfrage
def create_base_params(genre_ids, popularity):
    params = {
        "with_genres": ",".join(map(str, genre_ids)),
        "language": "de-DE",
        "sort_by": "popularity.desc" if popularity == "bekannt" else "popularity.asc",
        "page": 1
    }
    return params

# Funktion zum Hinzufügen des Jahrgangsfilters
def add_year_group_filter(params, year_group):
    if year_group == "älter":
        params["release_date.lte"] = "2000-01-01"
    elif year_group == "neuer":
        params["release_date.gte"] = "2000-01-01"
    return params

# Funktion zum Hinzufügen des Produktionsfirmenfilters
def add_production_company_filter(params, production_company_id):
    if production_company_id:
        params["with_companies"] = production_company_id
    return params

# Funktion zum Hinzufügen des Streaminganbieterfilters
def add_streaming_provider_filter(params, streaming_provider_id):
    if streaming_provider_id:
        params["with_watch_providers"] = streaming_provider_id
        params["watch_region"] = "DE"
    return params

# Funktion zum Hinzufügen des Laufzeitfilters
def add_runtime_filter(params, runtime_range):
    if runtime_range:
        min_runtime, max_runtime = runtime_range
        params["with_runtime.gte"] = min_runtime
        params["with_runtime.lte"] = max_runtime
    return params

# Hauptfunktion zum Abrufen der Filme basierend auf den Filtern
def get_top_movies_by_genre(
    genre_ids,
    year_group,
    popularity="bekannt",
    streaming_provider_id=None,
    production_company_id=None,
    runtime_range=None,
    max_movies=10
):
    movie_discover_url = f"{url}/discover/movie"
    params = create_base_params(genre_ids, popularity)
    params = add_year_group_filter(params, year_group)
    params = add_production_company_filter(params, production_company_id)
    params = add_streaming_provider_filter(params, streaming_provider_id)
    params = add_runtime_filter(params, runtime_range)

    all_movies = []
    while len(all_movies) < max_movies:
        response_data = make_request(movie_discover_url, params)
        if not response_data:
            break

        movies = response_data.get("results", [])
        if not movies:
            break

        for movie in movies:
            imdb_id = get_imdb_id_from_tmdb(movie.get("id"))
            if imdb_id:
                title = movie.get("title") or movie.get("original_title")
                print(f"Film: {title}, IMDb-ID: {imdb_id}")
                all_movies.append(movie)

        params["page"] += 1
        if params["page"] > response_data.get("total_pages", 1):
            break

    # Zufällige Auswahl der Filme
    if all_movies:
        return random.sample(all_movies, min(len(all_movies), max_movies))
    else:
        return []


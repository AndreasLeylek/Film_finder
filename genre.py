from TMDB import url, BEARER_TOKEN, make_request
import requests




def get_genre_id(genre_name):
    genres = {
        "action": 28,
        "adventure": 12,
        "animation": 16,
        "comedy": 35,
        "crime": 80,
        "documentary": 99,
        "drama": 18,
        "family": 10751,
        "fantasy": 14,
        "history": 36,
        "horror": 27,
        "music": 10402,
        "mystery": 9648,
        "romance": 10749,
        "science fiction": 878,
        "tv movie": 10770,
        "thriller": 53,
        "war": 10752,
        "western": 37,
    }
    return genres.get(genre_name.lower(), None)

def get_genre_combination(genre, mood):
    genre_map = {
        "Action": {
            "Fröhlich": [28, 35],
            "Spannend": [28, 53],
            "Nachdenklich": [28, 18],
            "Inspirierend": [28, 12],
            "Liebe": [28, 10749],
            "Psycho": [28, 27],
            "Krieg": [28, 10752],
        },
        "Science Fiction": {
            "Fröhlich": [878, 35],
            "Spannend": [878, 53],
            "Nachdenklich": [878, 18],
            "Inspirierend": [878, 12],
            "Liebe": [878, 10749],
            "Psycho": [878, 27],
        },
        "Adventure": {
            "Fröhlich": [12, 35],
            "Spannend": [12, 53],
            "Nachdenklich": [12, 18],
            "Inspirierend": [12, 36],
            "Liebe": [12, 10749],
        },
        "Drama": {
            "Fröhlich": [18, 35],
            "Spannend": [18, 53],
            "Nachdenklich": [18, 9648],
            "Inspirierend": [18, 36],
            "Liebe": [18, 10749],
            "Psycho": [18, 27],
        },
        "Comedy": {
            "Fröhlich": [35, 12],
            "Spannend": [35, 53],
            "Nachdenklich": [35, 18],
            "Inspirierend": [35, 10402],
            "Liebe": [35, 10749],
        },
        "Horror": {
            "Spannend": [27, 53],
            "Psycho": [27, 9648],
            "Krieg": [27, 10752],
            "Mystery": [27, 9648],
        },
        "Romance": {
            "Fröhlich": [10749, 35],
            "Spannend": [10749, 53],
            "Nachdenklich": [10749, 18],
            "Inspirierend": [10749, 36],
        },
        "Thriller": {
            "Spannend": [53, 28],
            "Psycho": [53, 27],
            "Nachdenklich": [53, 18],
            "Mystery": [53, 9648],
            "Krieg": [53, 10752],
        },
        "Family": {
            "Fröhlich": [10751, 35],
            "Inspirierend": [10751, 18],
            "Fantasy": [10751, 14],
        },
        "Fantasy": {
            "Fröhlich": [14, 35],
            "Spannend": [14, 53],
            "Liebe": [14, 10749],
            "Mystery": [14, 9648],
        },
        "Animation": {
            "Fröhlich": [16, 35],
            "Abenteuerlich": [16, 12],
            "Familienfreundlich": [16, 10751],
            "Inspirierend": [16, 18],
        },
        "Documentary": {
            "Nachdenklich": [99, 18],
            "Inspirierend": [99, 36],
            "Abenteuerlich": [99, 12],
        },
        "War": {
            "Nachdenklich": [10752, 18],
            "Psycho": [10752, 27],
            "Spannend": [10752, 53],
        },
        "Western": {
            "Abenteuerlich": [37, 12],
            "Spannend": [37, 53],
            "Krieg": [37, 10752],
        },
    }

    # Rückgabe der Kombination, wenn vorhanden
    return genre_map.get(genre, {}).get(mood, [])


def update_mood(selected_genre):
    genre_map = get_genre_combination()
    return list(genre_map.get(selected_genre, {}).key())


# Alle verfügbaren Genres abrufen
def get_genres():
    genre_url = f"{url}/genre/movie/list"
    params = {"language": "de-DE"}
    return make_request(url, params).get("genres", [])
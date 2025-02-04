from TMDB import url, make_request, BEARER_TOKEN
import requests

# Streaming-Provider abrufen
def get_streaming_providers():
    streaming_url = f"{url}/watch/providers/movie"
    params = {"language": "de", "watch_region": "DE"}
    return make_request(url, params).get("results", [])

# Streaming-Provider-ID basierend auf Namen abrufen
def get_streaming_provider_id(streaming_service_name):
    provider_map = {
        "netflix": 8,
        "amazon prime": 9,
        "disney+": 337,
        "hulu": 15,
        "hbo max": 384,
        "apple itunes": 2,
        "google play movies": 3,
        "youtube": 188,
        "apple tv+": 350,
        "sky go": 19,
        "peacock": 386,
        "paramount+": 531,
        "mubi": 421,
        "crave": 230,
        "starz": 43,
    }
    return provider_map.get(streaming_service_name.lower())


# def get_streaming_provider_url(movie_id, provider_name):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
#     headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
#
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         providers_data = response.json().get('results', {}).get('DE', {})
#         if 'flatrate' in providers_data:
#             for provider in providers_data['flatrate']:
#                 if provider['provider_name'].lower() == provider_name.lower():
#                     # Beispiel-URL für den Streaming-Service (anpassbar)
#                     return f"https://www.{provider_name.lower().replace(' ', '')}.com"
#     else:
#         print(f"Fehler beim Abrufen der Streaming-Anbieter: {response.status_code}")
#     return None

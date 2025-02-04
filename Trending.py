import customtkinter as ctk
import requests
from tkinter import messagebox
from TMDB import BEARER_TOKEN  # API-Token importieren
from Popup import show_movie_popup  # Import der show_movie_popup Funktion für Details


# Funktion zum Abrufen der angesagten Filme von TMDB
def fetch_trending_movies():
    all_movies = []
    page = 1
    while len(all_movies) < 100:  # Schleife läuft, bis 100 Filme erreicht sind
        url = f"https://api.themoviedb.org/3/trending/movie/day?page={page}"
        headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            all_movies.extend(data.get("results", []))  # Filme zur Liste hinzufügen

            # Überprüfen, ob es weitere Seiten gibt
            if page >= data.get("total_pages", 1):
                break  # Abbrechen, wenn keine weiteren Seiten vorhanden sind
            page += 1
        else:
            messagebox.showerror("Fehler", "Fehler beim Abrufen der Trending-Filme.")
            break

    return all_movies[:100]  # Nur die ersten 100 Filme zurückgeben



# Funktion zum Anzeigen der Trending-Filme
def show_trending_movies():
    trending_movies = fetch_trending_movies()
    trending_popup = ctk.CTkToplevel()
    trending_popup.title("Aktuell angesagte Filme")
    trending_popup.geometry("700x600")
    trending_popup.attributes('-topmost', True)
    trending_popup.after(500, lambda: trending_popup.attributes('-topmost', False))

    # Scrollbarer Frame für die Filme
    scrollable_frame = ctk.CTkScrollableFrame(trending_popup)
    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Kopfzeile
    ctk.CTkLabel(scrollable_frame, text="Titel", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, padx=5, pady=5,
                                                                                      sticky="w")
    ctk.CTkLabel(scrollable_frame, text="Erscheinungsjahr", font=('Helvetica', 12, 'bold')).grid(row=0, column=1,
                                                                                                 padx=5, pady=5,
                                                                                                 sticky="w")
    ctk.CTkLabel(scrollable_frame, text="Bewertung", font=('Helvetica', 12, 'bold')).grid(row=0, column=2, padx=5,
                                                                                          pady=5, sticky="w")

    # Filmdaten hinzufügen
    for idx, movie in enumerate(trending_movies, start=1):
        title = movie.get("title", "Kein Titel")
        release_date = movie.get("release_date", "Unbekannt")[:4]
        rating = movie.get("vote_average", "N/A")

        # Zeilen anzeigen
        ctk.CTkLabel(scrollable_frame, text=title).grid(row=idx, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(scrollable_frame, text=release_date).grid(row=idx, column=1, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(scrollable_frame, text=f"{rating}/10").grid(row=idx, column=2, padx=5, pady=5, sticky="w")

        # "Mehr"-Button zum Anzeigen der Film-Details
        ctk.CTkButton(scrollable_frame, text="Mehr", command=lambda m=movie: show_movie_popup(m)).grid(row=idx,
                                                                                                       column=3, padx=5,
                                                                                                       pady=5,
                                                                                                       sticky="w")

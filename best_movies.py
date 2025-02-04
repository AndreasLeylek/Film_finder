import customtkinter as ctk
import requests
from tkinter import messagebox
from TMDB import BEARER_TOKEN  # API-Token importieren
from Popup import show_movie_popup  # Importiere die Funktion zum Anzeigen der Film-Details


# Top bewertete Filme aufrufen
def fetch_top_rated_movies():
    all_movies = []
    page = 1
    while len(all_movies) < 100:  #max 100 Filme
        url = f"https://api.themoviedb.org/3/movie/top_rated?page={page}"
        headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data_movies = response.json()
            all_movies.extend(data_movies.get("results", []))  # Filme zur Liste hinzufügen

            # Überprüfen, ob es weitere Seiten gibt
            if page >= data_movies.get("total_pages", 1):
                break  # Abbrechen, wenn keine weiteren Seiten vorhanden sind
            page += 1
        else:
            messagebox.showerror("Fehler", "Fehler beim Abrufen der Trending-Filme.")
            break

    return all_movies[:100]  # Nur die ersten 100 Filme zurückgeben


# Funktion zum Anzeigen der Top-Rated-Filme
def show_top_rated_movies():
    top_rated_movies = fetch_top_rated_movies()
    top_rated_popup = ctk.CTkToplevel()
    top_rated_popup.title("Top bewertete Filme")
    top_rated_popup.geometry("700x600")
    top_rated_popup.attributes('-topmost', True)
    top_rated_popup.after(500, lambda: top_rated_popup.attributes('-topmost', False))

    # Scrollbarer Frame für die Filme
    scrollable_frame = ctk.CTkScrollableFrame(top_rated_popup)
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
    for idx, movie in enumerate(top_rated_movies, start=1):
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

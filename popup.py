import customtkinter as ctk
from customtkinter import CTkImage
import requests
from io import BytesIO
from PIL import Image
from tkinter import  messagebox
from TMDB import get_imdb_id_from_tmdb
from web_logger import scrape_imdb_description
import webbrowser

# Funktion zum Herunterladen des Posters und Rückgabe als CTkImage
def load_poster(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        img = Image.open(image_data).resize((300, 400), Image.Resampling.LANCZOS)
        return CTkImage(img, size=(300, 400))
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Laden des Posters: {e}")
    except Exception as e:
        print(f"Allgemeiner Fehler beim Laden des Posters: {e}")
    return None


def show_movie_popup(movie):
    if not movie:
        messagebox.showinfo("Fehler", "Kein Film gefunden.")
        return

    popup = ctk.CTkToplevel()
    popup.title("Filmdetails")
    popup.geometry("550x700")
    # popup.lift()
    popup.attributes('-topmost', True)
    popup.after(500, lambda: popup.attributes('-topmost', False))



    # Titel zentriert oben
    title = movie.get('title') or movie.get('original_title') or "Kein Titel verfügbar"
    release_date = movie.get('release_date', '')[:4] if movie.get('release_date') else 'Unbekannt'
    ctk.CTkLabel(popup, text=f"{title} ({release_date})", font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=3, pady=(10, 20), sticky="n")

    # Bewertung und Film ansehen Button nebeneinander unter dem Titel
    rating = movie.get('vote_average', 'Keine Bewertung verfügbar')
    ctk.CTkLabel(popup, text=f"Bewertung: {rating}/10", font=('Helvetica', 12)).grid(row=1, column=0, padx=10, pady=(5, 10), sticky="e")

    # TMDB-URL für den Film
    movie_id = movie.get('id')
    tmdb_url = f"https://www.themoviedb.org/movie/{movie_id}/watch"

    # Button für TMDB-Seite
    ctk.CTkButton(popup, text="Film ansehen", command=lambda: webbrowser.open(tmdb_url)).grid(row=1, column=1, padx=10, pady=(5, 10), sticky="w")

    # Poster zentriert in der nächsten Zeile
    poster_url = f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}" if movie.get('poster_path') else None
    if poster_url:
        poster_img = load_poster(poster_url)
        if poster_img:
            poster_label = ctk.CTkLabel(popup, image=poster_img, text=" ")
            poster_label.image = poster_img
            poster_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="n")
        else:
            ctk.CTkLabel(popup, text="Kein Poster verfügbar").grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="n")

    # Beschreibung unter dem Poster
    imdb_id = get_imdb_id_from_tmdb(movie.get('id'))
    description = scrape_imdb_description(imdb_id) if imdb_id else 'Keine IMDb-Beschreibung verfügbar'
    ctk.CTkLabel(popup, text=f"Beschreibung: {description}", wraplength=500, justify="left").grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nw")

    # "Schließen" Button ganz unten zentriert
    ctk.CTkButton(popup, text="Schließen", command=popup.destroy).grid(row=4, column=0, columnspan=3, pady=(20, 10), sticky="s")



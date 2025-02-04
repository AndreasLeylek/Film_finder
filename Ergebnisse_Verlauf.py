import webbrowser
from PIL import Image
from customtkinter import CTkImage, CTkToplevel, CTkLabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Database import get_saved_movies, get_movie_data_from_tmdb, searches_per_genre
import customtkinter as ctk
from tkinter import messagebox
from collections import Counter
import matplotlib.pyplot as plt
from Popup import load_poster
from TMDB import get_imdb_id_from_tmdb
from web_logger import scrape_imdb_description

# Wörterbuch zum Zählen der Genre-Suchen
genre_search_count = Counter()

def show_genre_bar_chart():
    genre_names, counts = searches_per_genre()
    if not genre_names or not counts:
        messagebox.showinfo("Keine Daten", "Keine Genre-Suchen vorhanden.")
        return

    chart_window = ctk.CTkToplevel()
    chart_window.title("Genre Diagramm")
    chart_window.geometry("1200x600")
    chart_window.attributes('-topmost', True)
    chart_window.after(500, lambda: chart_window.attributes('-topmost', False))

    # Configure grid
    chart_window.grid_rowconfigure(1, weight=1)
    chart_window.grid_columnconfigure(0, weight=1)

    title_label = ctk.CTkLabel(chart_window, text="Häufigkeit der Genre-Suchen", font=("Helvetica", 18, "bold"))
    title_label.grid(row=0, column=0, pady=10)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(genre_names, counts, color='skyblue')
    ax.set_xlabel("Anzahl der Suchen", fontsize=12)
    ax.set_ylabel("Genre", fontsize=12)
    ax.invert_yaxis()
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")

def show_saved_movies():
    movies = get_saved_movies()
    if not movies:
        messagebox.showinfo("Keine Einträge", "Es sind keine gespeicherten Filme vorhanden.")
        return

    history_popup = ctk.CTkToplevel()
    history_popup.title("Gespeicherte Filme")
    history_popup.geometry("1150x650")
    history_popup.attributes('-topmost', True)
    history_popup.after(500, lambda: history_popup.attributes('-topmost', False))

    # Configure grid
    history_popup.grid_rowconfigure(1, weight=1)
    history_popup.grid_columnconfigure(0, weight=1)

    # Table Frame
    table_frame = ctk.CTkScrollableFrame(history_popup)
    table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # Konfiguration der Spaltengewichte
    for col in range(7):
        table_frame.grid_columnconfigure(col, weight=1)

    # Laden des Icons
    original_icon = Image.open("kreisdiagramme.png")
    resized_icon = original_icon.resize((20, 20), Image.LANCZOS)
    icon_image = CTkImage(light_image=resized_icon, dark_image=resized_icon)

    headers = ["Nr.", "Titel", "Erscheinungsjahr", "IMDb ID", "Beschreibung", "Hinzugefügt am", ""]
    for col, header in enumerate(headers):
        label = ctk.CTkLabel(table_frame, text=header, font=('Helvetica', 12, 'bold'), anchor="w")
        label.grid(row=0, column=col, padx=5, pady=5, sticky="w")

    # Icon-Button in der Header-Zeile über den "Mehr"-Buttons
    icon_button = ctk.CTkButton(
        table_frame,
        text="",
        image=icon_image,
        width=30, height=30,
        command=show_genre_bar_chart)
    icon_button.image = icon_image
    icon_button.grid(row=0, column=6, padx=5, pady=5, sticky="e")

    for idx, movie in enumerate(movies, start=1):
        title, release_year, imdb_id, description, timestamp = movie

        ctk.CTkLabel(table_frame, text=str(idx)).grid(row=idx, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(table_frame, text=title).grid(row=idx, column=1, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(table_frame, text=str(release_year)).grid(row=idx, column=2, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(table_frame, text=imdb_id).grid(row=idx, column=3, padx=5, pady=5, sticky="w")

        short_description = description[:50] + "..." if len(description) > 50 else description
        ctk.CTkLabel(table_frame, text=short_description).grid(row=idx, column=4, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(table_frame, text=timestamp.strftime("%Y-%m-%d %H:%M")).grid(row=idx, column=5, padx=5, pady=5, sticky="w")

        ctk.CTkButton(
            table_frame,
            text="Mehr",
            command=lambda m_id=imdb_id: show_movie_popup(get_movie_data_from_tmdb(m_id))
        ).grid(row=idx, column=6, padx=5, pady=5, sticky="e")

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

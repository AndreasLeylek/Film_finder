import webbrowser
import customtkinter as ctk
from tkinter import messagebox
import requests
import threading
from TMDB import *
from streaming_provider import get_streaming_provider_id, get_streaming_providers
from company import search_company_by_name
from genre import get_genre_id, get_genre_combination
from popup import *
from db import get_movie_data_from_tmdb, insert_movie_with_relations, get_saved_movies
from history import show_saved_movies
from trending import show_trending_movies
from best_movies import show_top_rated_movies
from web_logger import scrape_imdb_description


# Hintergrund-API-Aufrufe und GUI-Aktualisierung
# Hintergrund-API-Aufrufe und Aktualisierung der GUI
def perform_api_calls_in_background(loading_window, progress_label, progress_bar, main_window):
    genre = genre_var.get()
    year_group = age_group_var.get().lower()
    mood = mood_var.get()
    streaming_service = streaming_service_var.get()
    production_company_name = production_company_entry.get()

    # Produktionsfirma suchen
    selected_company_id = None
    if production_company_name:
        companies = search_company_by_name(production_company_name)
        if companies:
            selected_company_id = companies[0]['id']
        else:
            main_window.after(0, lambda: messagebox.showinfo(
                "Fehler",
                f"Keine Produktionsfirma mit dem Namen '{production_company_name}' gefunden."
            ))
            loading_window.destroy()
            return

    # Streaminganbieter-ID abrufen
    streaming_provider_id = get_streaming_provider_id(streaming_service)
    if streaming_service and not streaming_provider_id:
        main_window.after(0, lambda: messagebox.showinfo("Fehler", "Streamingdienst nicht gefunden."))
        loading_window.destroy()
        return

    # Genre-Kombination basierend auf Stimmung abrufen
    genre_combination = get_genre_combination(genre, mood)

    # Sliderwert auslesen und in Laufzeitbereich umwandeln
    slider_value = int(runtime_slider.get())
    runtime_range = get_runtime_range(slider_value)

    # Ladebalken starten
    main_window.after(0, lambda: progress_label.configure(text="Lädt..."))
    main_window.after(0, progress_bar.start)

    # Filme abrufen
    movies = get_top_movies_by_genre(
        genre_combination,
        year_group,
        streaming_provider_id=streaming_provider_id,
        production_company_id=selected_company_id,
        runtime_range=runtime_range
    )

    # Ladebalken stoppen
    main_window.after(0, progress_bar.stop)
    main_window.after(0, loading_window.destroy)

    if movies:
        movie = movies[0]
        movie_data = get_movie_data_from_tmdb(movie['id'])
        if movie_data:
            insert_movie_with_relations(movie_data)
        main_window.after(0, lambda: show_movie_popup(movie))
    else:
        main_window.after(0, lambda: messagebox.showinfo("Keine Filme gefunden", "Es wurden keine Filme gefunden, die den Kriterien entsprechen."))

# Ladefenster erstellen
def show_loading_window(main_window):
    loading_window = ctk.CTkToplevel(main_window)
    loading_window.title("Laden...")
    loading_window.geometry("300x100")
    loading_window.lift()

    progress_label = ctk.CTkLabel(loading_window, text="Lädt...", font=("Helvetica", 12))
    progress_label.pack(pady=10)
    progress_bar = ctk.CTkProgressBar(loading_window)
    progress_bar.pack(pady=20)

    # Thread für API-Aufrufe starten
    threading.Thread(
        target=perform_api_calls_in_background,
        args=(loading_window, progress_label, progress_bar, main_window)
    ).start()

# API-Aufruf starten
def start_api_call():
    show_loading_window(main_window)


main_window = ctk.CTk() #Hauptfenster erstellen
# GUI-Einstellungen und Layout
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


main_window.title("Filmfinder")
main_window.geometry("550x350")

# Genre-Auswahl
ctk.CTkLabel(main_window, text="Genre").grid(row=0, column=0, padx=10, pady=5)
genre_var = ctk.StringVar(main_window) #Interaktion zwischen Variable und Widget
genre_var.set(" ")
genres = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama",
    "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance",
    "Science Fiction", "TV Movie", "Thriller", "War"
]
ctk.CTkOptionMenu(main_window, variable=genre_var, values=genres).grid(row=0, column=1, padx=10, pady=5)

# Altersgruppe-Auswahl
ctk.CTkLabel(main_window, text="Alter des Films").grid(row=1, column=0, padx=10, pady=5)
age_group_var = ctk.StringVar(main_window)
age_group_var.set("")
ctk.CTkOptionMenu(main_window, variable=age_group_var, values=["Älter", "Neuer", " "]).grid(row=1, column=1, padx=10, pady=5)

# Stimmung-Auswahl
ctk.CTkLabel(main_window, text="Stimmung").grid(row=2, column=0, padx=10, pady=5)
mood_var = ctk.StringVar(main_window)
mood_var.set("")
ctk.CTkOptionMenu(
    main_window,
    variable=mood_var,
    values=["Fröhlich", "Spannend", "Nachdenklich", "Inspirierend", "Krieg", " "]
).grid(row=2, column=1, padx=10, pady=5)

# Streamingdienst-Auswahl
ctk.CTkLabel(main_window, text="Streamingdienst").grid(row=3, column=0, padx=10, pady=5)
streaming_service_var = ctk.StringVar(main_window)
streaming_service_var.set(" ")
streaming_services = ["Netflix", "Amazon Prime", "Disney+", "Apple TV+", "Paramount+"]
ctk.CTkOptionMenu(main_window, variable=streaming_service_var, values=streaming_services).grid(row=3, column=1, padx=10, pady=5)

# Produktionsfirma-Eingabe
ctk.CTkLabel(main_window, text="Produktionsfirma").grid(row=4, column=0, padx=10, pady=5)
production_company_entry = ctk.CTkEntry(main_window)
production_company_entry.grid(row=4, column=1, padx=10, pady=5)

# Laufzeit-Slider
ctk.CTkLabel(main_window, text="Laufzeit (Stunden)").grid(row=5, column=0, padx=10, pady=5)
runtime_value_label = ctk.CTkLabel(main_window, text="Laufzeit:")
runtime_value_label.grid(row=5, column=2, padx=10, pady=5)

def update_runtime_label(value):
    options = ["0-1 Stunde", "1-2 Stunden", "2-3 Stunden", "3+ Stunden"]
    runtime_value_label.configure(text=f"Laufzeit: {options[int(float(value))-1]}")

runtime_slider = ctk.CTkSlider(
    main_window,
    from_=1,
    to=4,
    number_of_steps=3,
    command=update_runtime_label
)
runtime_slider.grid(row=5, column=1, padx=10, pady=5)
runtime_slider.set(2)  # Standardwert setzen
update_runtime_label(runtime_slider.get())

# Buttons
trending_button = ctk.CTkButton(main_window, text="Aktuell angesagt", command=show_trending_movies)
trending_button.grid(row=7, column=0, padx=10, pady=5)

top_rated_button = ctk.CTkButton(main_window, text="Beste Filme aller Zeiten", command=show_top_rated_movies)
top_rated_button.grid(row=7, column=1, padx=10, pady=5)

history_button = ctk.CTkButton(main_window, text="Verlauf anzeigen", command=show_saved_movies)
history_button.grid(row=9, column=2, columnspan=2, pady=20)

submit_button = ctk.CTkButton(main_window, text="Film finden", command=start_api_call)
submit_button.grid(row=7, column=2, columnspan=2, pady=20)

main_window.mainloop()









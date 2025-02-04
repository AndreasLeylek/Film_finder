import psycopg2
import requests
from TMDB import BEARER_TOKEN

# Datenbank- und TMDB-Konfiguration
DB_CONFIG = {
    "host": "localhost",
    "database": "TMDB",
    "user": "postgres",
    "password": "codersbay"
}

def connect_to_db():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        connection.autocommit = True
        return connection
    except Exception as e:
        print(f"Fehler bei der Verbindung zur Datenbank: {e}")
        return None

def create_database_if_not_exists():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="codersbay"
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'TMDB';")
        if not cursor.fetchone():
            cursor.execute('CREATE DATABASE "TMDB";')
            print("Datenbank 'TMDB' erfolgreich erstellt!")
        else:
            print("Datenbank 'TMDB' existiert bereits.")
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Fehler beim Erstellen der Datenbank: {e}")

def create_tables():
    connection = connect_to_db()
    if connection is None:
        print("Keine Verbindung zur Datenbank. Tabellen konnten nicht erstellt werden.")
        return

    try:
        with connection.cursor() as cursor:
            # Tabelle: genres
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS genres (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                );
            ''')
            # Tabelle: movies
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movies (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    release_year INT,
                    imdb_id VARCHAR(50),
                    description TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            # Tabelle: moviegenres
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS moviegenres (
                    movie_id INT,
                    genre_id INT,
                    PRIMARY KEY (movie_id, genre_id),
                    FOREIGN KEY (movie_id) REFERENCES movies (id),
                    FOREIGN KEY (genre_id) REFERENCES genres (id)
                );
            ''')
            # Tabelle: streamingservices
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS streamingservices (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                );
            ''')
            # Tabelle: moviestreaming
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS moviestreaming (
                    movie_id INT,
                    streaming_service_id INT,
                    PRIMARY KEY (movie_id, streaming_service_id),
                    FOREIGN KEY (movie_id) REFERENCES movies (id),
                    FOREIGN KEY (streaming_service_id) REFERENCES streamingservices (id)
                );
            ''')
            print("Alle Tabellen wurden erfolgreich erstellt!")
    except Exception as e:
        print(f"Fehler beim Erstellen der Tabellen: {e}")
    finally:
        connection.close()


def searches_per_genre():
    connection = connect_to_db()
    if connection is None:
        print("Keine Verbindung zur Datenbank.")
        return [], []

    try:
        with connection.cursor() as cursor:
            # Abfrage für Genre-Häufigkeiten
            query = """
                SELECT g.name, COUNT(mg.genre_id) as count
                FROM moviegenres mg
                JOIN genres g ON mg.genre_id = g.id
                GROUP BY g.name
                ORDER BY count DESC;
            """
            cursor.execute(query)
            results = cursor.fetchall()

            if not results:
                print("Keine Daten zum Anzeigen.")
                return [], []


            genres = [row[0] for row in results]
            counts = [row[1] for row in results]


    except Exception as e:
        print(f"Fehler beim Abrufen der Genre-Statistiken: {e}")
    finally:
        connection.close()

    return genres,counts

# Funktionen für Genre-Operationen
def insert_genre(genre_id, genre_name):
    """Fügt ein Genre in die Datenbank ein, falls es noch nicht existiert."""
    connection = connect_to_db()
    if connection is None:
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO genres (id, name) VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (genre_id, genre_name))
            connection.commit()
    except Exception as e:
        print(f"Fehler beim Einfügen des Genres: {e}")
    finally:
        connection.close()


# Funktionen für Streaming-Service-Operationen
def insert_streaming_service(service_id, service_name):
    """Fügt einen Streaming-Dienst in die Datenbank ein, falls er noch nicht existiert."""
    connection = connect_to_db()
    if connection is None:
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO streamingservices (id, name) VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (service_id, service_name))
            connection.commit()
    except Exception as e:
        print(f"Fehler beim Einfügen des Streaming-Dienstes: {e}")
    finally:
        connection.close()


# Funktion zum Einfügen eines Films und seiner Beziehungen (Genres und Streaming-Dienste)
def insert_movie_with_relations(movie_data):
    """Fügt einen Film und seine Beziehungen (Genres, Streaming-Dienste) in die Datenbank ein."""
    connection = connect_to_db()
    if connection is None:
        return

    try:
        with connection.cursor() as cursor:
            # Film einfügen
            cursor.execute("""
                INSERT INTO movies (id, title, release_year, imdb_id, description)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (
                movie_data['id'],
                movie_data['title'],
                movie_data.get('release_year'),
                movie_data.get('imdb_id'),
                movie_data.get('overview', '')
            ))

            # Genres und ihre Beziehungen einfügen
            for genre in movie_data.get('genres', []):
                insert_genre(genre['id'], genre['name'])
                cursor.execute("""
                    INSERT INTO moviegenres (movie_id, genre_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING;
                """, (movie_data['id'], genre['id']))

            # Streaming-Dienste und ihre Beziehungen einfügen
            if 'streaming_services' in movie_data:
                for service in movie_data['streaming_services']:
                    insert_streaming_service(service['id'], service['name'])
                    cursor.execute("""
                        INSERT INTO moviestreaming (movie_id, streaming_service_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING;
                    """, (movie_data['id'], service['id']))

            connection.commit()
            print(f"Film {movie_data['title']} mit Beziehungen erfolgreich eingefügt.")
    except Exception as e:
        print(f"Fehler beim Einfügen des Films und der Beziehungen: {e}")
    finally:
        connection.close()


# Funktion zum Abrufen der Filmdaten von TMDB
def get_movie_data_from_tmdb(movie_id):
    """Holt Filmdaten von TMDB basierend auf der Movie-ID."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        movie_data = response.json()

        # Extrahiere das Jahr aus dem release_date
        release_date = movie_data.get('release_date', None)
        movie_data['release_year'] = release_date.split("-")[0] if release_date else None

        # Beispiel für Streaming-Dienst-Daten (muss entsprechend hinzugefügt werden)
        movie_data['streaming_services'] = []  # Platzhalter für echte Streaming-Dienste

        return movie_data
    else:
        print(f"Fehler: {response.status_code}")
        return None


# Funktion zum Abrufen gespeicherter Filme
def get_saved_movies(limit=1000):
    """Ruft die letzten gespeicherten Filme aus der Datenbank ab."""
    connection = connect_to_db()
    if connection is None:
        print("Keine Verbindung zur Datenbank.")
        return []

    try:
        with connection.cursor() as cursor:
            select_query = """
                SELECT title, release_year, imdb_id, description, timestamp
                FROM movies 
                ORDER BY timestamp desc
                LIMIT %s;
            """
            cursor.execute(select_query, (limit,))
            movies = cursor.fetchall()
            return movies
    except Exception as e:
        print(f"Fehler beim Abrufen der gespeicherten Filme: {e}")
        return []
    finally:
        connection.close()
if __name__ == "__main__":
    create_database_if_not_exists()
    create_tables()  # Erstellt Schema und Tabellen




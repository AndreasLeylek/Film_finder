# MiniProject: FilmFinder

# Filmfinder
Ein interaktives Python-Projekt zur Suche nach Filmen basierend auf einer Vielzahl von Filtern wie Genre, Produktionsfirma, Streamingdienst, Veröffentlichungsjahr, Stimmung und Laufzeit. Die Anwendung nutzt die TMDb-API, um relevante Filme abzurufen und eine benutzerfreundliche GUI bereitzustellen.

# Inhaltsverzeichnis
- [über das Projekt](#über-das-projekt)
- [Technologien](#technologien)
- [Funktionen](#funktionen)
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Projektstruktur](#projektstruktur)
- [API-Konfiguration](#api-konfiguration)
- [Datenbank](#datenbank)
- [Bekannte Probleme](#bekannte-probleme)
- [Docker Connection](#docker-connection)

# über das Projekt
Filmfinder ist ein benutzerfreundliches Tool, das es ermöglicht, gezielt Filme zu suchen und zu finden. Die Anwendung bietet Filteroptionen für Genre, Streaminganbieter, Produktionsfirma, Stimmung und Laufzeit. Die Filmdaten werden mithilfe der TMDb-API abgerufen und die Ergebnisse können in einem Popup-Fenster angezeigt werden.

# Technologien
**Programmiersprache:** Python

**GUI-Framework:** CustomTkinter

**API:** TMDb (The Movie Database)

**Datenbank:** PostgreSQL

# Funktionen
**Film-Suche:** Finde Filme basierend auf Genre, Produktionsfirma, Streamingdienst, Veröffentlichungsjahr, Stimmung und Laufzeit.


**[Trend-Anzeige:](https://www.themoviedb.org/movie)** Zeige aktuelle, beliebte Filme an.


**[Top-Filme:](https://www.themoviedb.org/movie/top-rated)** Zeige die bestbewerteten Filme an.


**Verlauf:** Speichere und zeige den Verlauf der gesuchten Filme.


**Pop-up-Benachrichtigungen:** Informiere den Benutzer über den Status der API-Anfragen und die Suchergebnisse.
# Installation
### Repository klonen:

```bash

git clone https://github.com/andreasleylek/miniproject.git
```
# Virtuelle Umgebung erstellen:

```bash
python -m venv NameDerVirtuellenUmgebung
venv\Scripts\activate  # Für Windows
```

### Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```
**TMDb-API konfigurieren:** Füge deinen Bearer-Token in der Datei API_KEY_URL.py ein.

# Verwendung
## Starte die Anwendung:
```bash
python main.py
```
#### GUI-Bedienung:
**Genre auswählen**: Wähle das Genre des Films.

**Alter des Films:** Wähle, ob der Film älter oder neuer sein soll.


**Stimmung:** Wähle eine passende Stimmung aus.


**Streamingdienst:** Wähle den bevorzugten Streaminganbieter.


**Produktionsfirma:** Gib eine Produktionsfirma ein (optional).


**Laufzeit-Slider:** Bestimme die Laufzeit des Films.


Klicke auf **"Film finden"**, um die Suche zu starten.
# Projektstruktur
**main.py:** Hauptskript, das die GUI erstellt und API-Anfragen verarbeitet.


**TMDB.py:** Schnittstelle zur TMDb-API.


**Streaming_Provider.py:** Funktionen für die Verarbeitung von Streaminganbietern.


**Company.py:** Funktionen zur Produktionsfirmensuche.


**Genre.py:** Genre-Verwaltungsfunktionen.


**Popup.py:** Anzeige von Popup-Benachrichtigungen.


**Database.py:** Speichern und Abrufen von Filmdaten.


**Ergebnisse_Verlauf.py:** Verlauf der gespeicherten Filme.


**Trending.py:** Anzeige aktueller Trends.


**best_movies.py:** Anzeige der besten Filme.


**web_logger.py:** IMDb-Filmbeschreibungsscraper.

# Api-Konfiguration
Die FilmFinder-Anwendung nutzt die TMDb-API, um Filminformationen abzurufen. Damit die API funktioniert, musst du einen Bearer-Token konfigurieren. Hier sind die Schritte, wie du das machst:

### Erstelle einen Account bei TMDb:
Gehe auf [The Movie Database](https://www.themoviedb.org) (TMDb) und registriere dich, falls du noch keinen Account hast.

Hole deinen API-Schlüssel:

Melde dich an und gehe zu deinem Profil.

Navigiere zu den API-Einstellungen und erhalte deinen Bearer-Token.

Konfiguriere den API-Schlüssel im Projekt:

Erstelle eine Datei **API_KEY_URL** im Projektordner.

Trage deinen Bearer-Token in den Code ein:


    BEARER_TOKEN = 
    HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    url = "https://api.themoviedb.org/3"
Speichere die Änderungen und stelle sicher, dass der Token korrekt ist.

**Hinweis:** Dein Bearer-Token sollte privat bleiben. Teile ihn nicht öffentlich und speichere ihn sicher.

# Datenbank
Die Anwendung verwendet eine PostgreSQL-Datenbank, um Filmdaten und deren Beziehungen (Genres, Streaming-Dienste) zu speichern. Hier ist, wie die Datenbank im Projekt eingerichtet und verwaltet wird:

### Konfiguration der Datenbank
#### 1. PostgreSQL herunterladen und installieren:
   - Lade PostgreSQL von der offiziellen Website herunter: [PostgreSQL](https://www.postgresql.org/download/)
   - Folge der Installationsanleitung und richte einen Benutzer sowie eine Datenbank ein.
#### 2.  PostgreSQL-Verbindungseinstellungen:
   - Die Verbindungsdetails für deine Datenbank sind in DB_CONFIG definiert:
       
       
       DB_CONFIG = {
           "host": "localhost",
           "database": "TMDB",
           "user": "postgres",
           "password": "codersbay"
       }
- Passe diese Werte entsprechend deinen PostgreSQL-Einstellungen an.

### Schritte zur Einrichtung der Datenbank
1. **Datenbank erstellen:**
   - Das Skript create_database_if_not_exists() überprüft, ob die Datenbank TMDB existiert, und erstellt sie gegebenenfalls.
   
2. **Tabellen erstellen:**
   - Das Skript create_tables() erstellt die erforderlichen Tabellen:
     - **genres:** Speichert Genre-Informationen.
     - **movies:** Speichert Filmdetails wie Titel, Erscheinungsjahr und Beschreibung.
     - **moviegenres:** Verknüpft Filme mit Genres.
     - **streamingservices:** Speichert Streaming-Dienst-Informationen.
     - **moviestreaming:** Verknüpft Filme mit Streaming-Diensten.
### Verwendung der Datenbank
1. **Verbindung zur Datenbank herstellen:**
   - Die Funktion connect_to_db() stellt eine Verbindung zu deiner PostgreSQL-Datenbank her.
2. **Tabellen erstellen und Daten verwalten:**
   - **create_tables():** Erstellt alle benötigten Tabellen.
   - **insert_movie_with_relations(movie_data):** Fügt einen Film und seine Beziehungen (Genres und Streaming-Dienste) in die Datenbank ein.
   - **searches_per_genre():** Zählt, wie oft jedes Genre gesucht wurde.
3. **Beispiel für Datenoperationen:**
   - **Genres einfügen:**  insert_genre(genre_id, genre_name)
   - **Streaming-Dienste einfügen:** insert_streaming_service(service_id, service_name)
   - **Filme einfügen:** Die Film- und Beziehungsdaten werden mithilfe von insert_movie_with_relations() in die Datenbank eingefügt.
### Wichtige Hinweise
   - **PostgreSQL installieren:** Stelle sicher, dass PostgreSQL auf deinem System installiert und der Datenbankserver läuft. Nutze den Link oben, um PostgreSQL herunterzuladen.
   - **Datenbankverbindung:** Falls die Verbindung fehlschlägt, überprüfe deine PostgreSQL-Einstellungen (Benutzername, Passwort und Datenbankname).

### Bekannte Probleme

**401-Fehler:** Falscher oder ungültiger API-Schlüssel. Überprüfe deinen Bearer-Token.

**204-Fehler:** Verbindung erfolgreich. Keine Ergebnisse

**Keine Filme gefunden:** Passe die Filtereinstellungen an, um bessere Ergebnisse zu erhalten.

## Docker Connection

Für die Ausführung der GUI-Anwendung in einem Docker-Container und die Anzeige auf einem virtuellen Desktop wird XMing benötigt, um das X-Server-Protokoll unter Windows zu unterstützen.

## Vorraussetzungen
- **Installiere XMing:**
    - Lade XMing von der offiziellen Webseite herunter: [XMing](https://sourceforge.net/projects/xming/)
    - Installiere XMing und starte es, bevor du die Docker-Befehle ausführst
##### Docker run Befehl für virtuellen Desktop mit ip- adresse:
```bash
docker run -it --rm -e DISPLAY=ip_adresse.1:0.0 miniproject

```
**Hinweis:** Um deine IP-Adresse herauszufinden, verwende den Befehl: 
```bash
ipconfig
````
Suche nach **IPv4-Adresse** zb. 172.30.224

##### Docker run Befehl für virtuellen Desktop mit host.docker.internal:
```bash 
docker run -it --rm -e DISPLAY=host.docker.internal.1:0.0 miniproject
```
**Hinweis:** Ersetze ip_adresse durch host.docker.internal 

## Erklärung
- **XMing:** Ein X-Server für Windows, der erforderlich ist, um die GUI-Anzeigen aus einem Docker-Container zu verwenden.
- **Vor der Ausführung:** Stelle sicher, dass XMing läuft, damit die Anwendung die GUI korrekt anzeigen kann.



 

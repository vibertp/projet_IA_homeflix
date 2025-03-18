import requests
import duckdb
import pandas as pd
from time import sleep

# API_KEY = "8c0a1e57719313fec82c077243f8f31b"
DB_FILE = "movies_db.duckdb"

def fetch_movie_data(movie_id):
    """Récupère les informations d'un film via l’API TMDB."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    
    
    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4YzBhMWU1NzcxOTMxM2ZlYzgyYzA3NzI0M2Y4ZjMxYiIsIm5iZiI6MTc0MjE5ODgxOS44NjA5OTk4LCJzdWIiOiI2N2Q3ZDgyMzE5MTg2OGM1NGZmMWMwOWIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.d-IUNeHmoALNyUtgOoTs-AU2vW87guSX1eNzcLdyTUc"
    
    }
    
    response = requests.get(url,headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur lors de la récupération du film ID {movie_id}: {response.status_code}")
        return None

def create_tables():
    """Crée les tables dans DuckDB si elles n'existent pas."""
    conn = duckdb.connect(DB_FILE)
    conn.execute("""
        CREATE or REPLACE TABLE films (
            id INT PRIMARY KEY,
            title TEXT,
            description TEXT,
            genres TEXT,
            release_date DATE,
            vote_average FLOAT,
            vote_count INT
        );
    """)
    conn.execute("""
        CREATE OR REPLACE TABLE ratings (
                user_id INT,
                film_id INT,
                rating FLOAT,
                timestamp INT
        );
    """)
    conn.close()

def save_movie_to_db(movie_data):
    """Enregistre les données d'un film dans DuckDB."""
    release_date = movie_data.get("release_date")
    if release_date == "" :
        release_date = None
    conn = duckdb.connect(DB_FILE)
    conn.execute("""
        INSERT INTO films (id, title, description, genres, release_date,vote_average, vote_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        movie_data['id'],
        movie_data['title'],
        movie_data['overview'],
        [g['name'] for g in movie_data['genres']],
        release_date,
        movie_data['vote_average'],
        movie_data['vote_count']
    ))
    conn.close()

import duckdb

def save_ratings_to_db(ratings_df):
    """Enregistre les notes du fichier CSV dans DuckDB."""
    conn = duckdb.connect(DB_FILE)
    
    # Créer la table 'ratings' si elle n'existe pas déjà
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            user_id INT,
            film_id INT,
            rating FLOAT,
            timestamp INT
        );
    """)
    
    # Insérer les données du DataFrame directement dans la table 'ratings'
    conn.register('ratings_df', ratings_df)  # Enregistrer le DataFrame en tant que table temporaire
    conn.execute("""
        INSERT INTO ratings
        SELECT * FROM ratings_df;
    """)
    
    conn.close()



def main():
    nmax = 500
    # Créer les tables dans la base de données DuckDB
    create_tables()

    # Charger le fichier CSV
    ratings_df = pd.read_csv("data/ratings.csv")
    
    # Récupérer les films uniques du fichier CSV
    unique_movie_ids = ratings_df['movieId'].unique()[:nmax]
    ratings_df = ratings_df[ratings_df["movieId"].isin(unique_movie_ids)]
    save_ratings_to_db(ratings_df)
    print("Importation des notes terminée.")

    for movie_id in unique_movie_ids:
        movie_data = fetch_movie_data(movie_id)
        
        if movie_data:
            save_movie_to_db(movie_data)
            print(f"Film '{movie_data['title']}' ajouté avec succès.")
        
        sleep(0.2)  # Pause pour éviter de dépasser le taux limite de l’API

    print("Importation terminée.")

if __name__ == "__main__":
    main()

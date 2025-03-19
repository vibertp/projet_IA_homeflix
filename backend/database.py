import requests
import duckdb
import pandas as pd
from loguru import logger
from time import sleep
import utils.config as config

def fetch_movie_data(movie_id:int) -> dict:
    """
    Récupère les informations d'un film via l’API TMDB.
    
    Args:
        movie_id (int) : identifiant du film 
    
    Return:
        .json ou None : information du film en fichier .json ou None si l'id ne correspond à aucun film.
    """
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    
    
    headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {config.API_KEY}"
    
    }
    
    response = requests.get(url,headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Erreur lors de la récupération du film ID {movie_id}: {response.status_code}")
        return None

def create_tables() -> None:
    """
    Crée les tables dans DuckDB ou les écrase si elle existe déjà.
    """
    conn = duckdb.connect(config.DB_FILE)
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

def save_movie_to_db(movie_data:dict) -> None:
    """
    Enregistre les données d'un film dans DuckDB.
    
    Args:
        movie_data (dict) : dictionnaire contenant toutes les informations du film.
    """
    release_date = movie_data.get("release_date")
    if release_date == "" :
        release_date = None
    genres = [g['name'] for g in movie_data['genres']]
    if not genres:
        genres = None
    conn = duckdb.connect(config.DB_FILE)
    conn.execute("""
        INSERT INTO films (id, title, description, genres, release_date,vote_average, vote_count)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        movie_data['id'],
        movie_data['title'],
        movie_data['overview'],
        genres,
        release_date,
        movie_data['vote_average'],
        movie_data['vote_count']
    ))
    conn.close()


def save_ratings_to_db(ratings_df:pd.DataFrame) -> None:
    """
    Enregistre les notes de ratings dans DuckDB.
    
    Args:
        ratings_df(pd.DataFrame)
    """
    conn = duckdb.connect(config.DB_FILE)
    
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
    
def unique_movie_id_in_ratings(nmax: int,df: pd.DataFrame) -> tuple:
    """Génère la liste des nmax premiers id de films uniques présents dans df.

    Args:
        nmax (int): nombre d'id max à prendre 
        df (pd.DataFrame): dataframe qui contient des id de films

    Returns:
        pd.DataFrame, np.array: retourne la liste des nmax identifiants uniques de films ainsi que 
        le dataframe filtrer sur ces id.
    """
    unique_movie_ids = df['movieId'].unique()[:nmax]
    df = df[df["movieId"].isin(unique_movie_ids)]
    return df, unique_movie_ids
    
    

def import_movie_to_db(ids_unique:list) -> None:
    """Cherche les informations des films sur TDBM et enregistre les informations dans la base de données duckDB.

    Args:
        ids_unique (list): ids uniques des films à chercher.
    """
    for movie_id in ids_unique:
        movie_data = fetch_movie_data(movie_id)
        
        if movie_data:
            save_movie_to_db(movie_data)
            logger.info(f"Film '{movie_data['title']}' ajouté avec succès.")
        
        sleep(0.2)  # Pause pour éviter de dépasser le taux limite de l’API

def supp_lignes_inutiles() -> None:
    """
    Supprime les lignes de la table ratings, dans la base de données, qui correspondent aux id de films inconnus pour TDBM.
    """
    conn = duckdb.connect(config.DB_FILE)
    conn.execute("""
                 DELETE 
                 FROM ratings 
                 WHERE film_id NOT IN (SELECT id FROM films)
                 """)
    conn.close()
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import duckdb
from sklearn.decomposition import TruncatedSVD
from loguru import logger
import pandas as pd
from backend.model import creation_model
import utils.config as config
from backend.predict import prediction

def seen_movies(userID):
    """
    Retourne les films déjà vus par un utilisateur donné.
    """
    logger.info("Chargement des données...")

    try:
        con = duckdb.connect(config.DB_FILE)
        ratings = con.execute("SELECT user_id, film_id, rating FROM ratings").df()
        films = con.execute("SELECT id, title FROM films").df()
        logger.info("Données chargées")
    except Exception as e:
        logger.error(f"Erreur de chargement des données: {e}")
    
    film_id_seen = ratings[ratings['user_id'] == userID][['film_id', 'rating']]

    list_films = []
    for film_id in film_id_seen['film_id']:
        title = films.loc[films['id'] == film_id, 'title'].values[0]
        list_films.append({
            "id": int(film_id),
            "title": title,
            "rating": float(film_id_seen.query(f'film_id == {film_id}')['rating'])
        })

    return {
        "user_id": int(userID),
        "recommendations": list_films
    }

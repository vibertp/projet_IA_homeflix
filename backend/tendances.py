import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import duckdb
from sklearn.decomposition import TruncatedSVD
from loguru import logger
import pandas as pd
import utils.config as config


def tendance(n=3):
    """
    Retourne les films déjà vus par un utilisateur donné.
    """
    logger.info("Chargement des données...")

    try:
        con = duckdb.connect(config.DB_FILE)
        films = con.execute("SELECT id, title, vote_count FROM films").df()
        logger.info("Données chargées")
    except Exception as e:
        logger.error(f"Erreur de chargement des données: {e}")
    
    popular_movies = films.sort_values(by='vote_count', ascending=False).head(n)

    return(popular_movies.to_dict(orient="records"))

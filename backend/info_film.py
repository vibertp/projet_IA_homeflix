import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import duckdb
from loguru import logger
import pandas as pd
import utils.config as config


def movie_info(filmID: int):
    """
    Retourne les informations d'un film donné.
    """
    logger.info("Chargement des données...")

    try:
        con = duckdb.connect(config.DB_FILE)
        films = con.execute("SELECT id, title, genres, description, release_date, vote_average FROM films").df()
        logger.info("Données chargées")
    except Exception as e:
        logger.error(f"Erreur de chargement des données: {e}")
    
    movie = films[films['id'] == filmID]

    return(movie.to_dict(orient="records")[0])

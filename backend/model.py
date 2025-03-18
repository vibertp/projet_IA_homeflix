
import duckdb
import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from loguru import logger
import joblib


def creation_model():
    """
    Crée un modèle de recommandation de films.
    """
    logger.add("debug.log", rotation="500 MB", level="DEBUG")

    logger.info("Connexion à la base DuckDB et chargement des données...")

    DB_FILE = "movies_db.duckdb"

    con = duckdb.connect("movies_db.duckdb")

    ratings_df = con.execute("SELECT user_id, film_id, rating FROM ratings").df()

    logger.info("Données chargées")
    con.close()

    logger.info("Transformation des données...")
    user_movie_matrix = ratings_df.pivot(index="user_id", columns="film_id", values="rating")

    logger.info("Création du modèle...")
    svd = TruncatedSVD(n_components=2, random_state=42)
    user_features = svd.fit_transform(user_movie_matrix)

    logger.info("Enregistrement du modèle...")
    joblib.dump(svd, "model.pkl")

    return(0)

import duckdb
import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from loguru import logger
import joblib
import utils.config as config


def creation_model():
    """
    Crée un modèle de recommandation de films.
    """
    logger.info("Connexion à la base DuckDB et chargement des données...")

    con = duckdb.connect(config.DB_FILE)

    ratings_df = con.execute("SELECT user_id, film_id, rating FROM ratings").df()

    logger.info("Données chargées")
    con.close()

    logger.info("Transformation des données...")
    user_movie_matrix = ratings_df.pivot(index="user_id", columns="film_id", values="rating").fillna(0)

    logger.info("Création du modèle...")
    svd = TruncatedSVD(n_components=50, random_state=42)
    user_film_svd = svd.fit_transform(user_movie_matrix)

    logger.info("Enregistrement du modèle...")
    try :
        joblib.dump(svd, 'model/svd_model.joblib')
        joblib.dump(user_film_svd, 'model/user_film_svd.joblib')
        logger.info("Modèle enregistré avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de l'enregistrement du modèle: {e}")
    return(0)

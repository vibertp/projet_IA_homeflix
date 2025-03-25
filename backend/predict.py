import duckdb
import pandas as pd
import numpy as np
from loguru import logger
import joblib
import utils.config as config

def prediction(user_id, n=3):
    logger.info("Chargement du modèle...")
    try :
        svd = joblib.load('model/svd_model.joblib')
        user_film_svd = joblib.load('model/user_film_svd.joblib')
        logger.info("Modèle chargé avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle: {e}")

    logger.info("Chargement des données...")
    con = duckdb.connect(config.DB_FILE)
    ratings_df = con.execute("SELECT user_id, film_id, rating FROM ratings").df()
    film_df = con.execute("SELECT id, title, description, release_date FROM films").df()
    con.close()
    user_film_matrix = ratings_df.pivot(index='user_id', columns='film_id', values='rating').fillna(0)

    logger.info("Calcul des prédictions...")
    try :
        predicted_ratings = svd.inverse_transform(user_film_svd)
        logger.info("Prédictions calculées avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors du calcul des prédictions: {e}")

    # Convertir les prédictions en DataFrame pour faciliter la manipulation
    predicted_ratings_df = pd.DataFrame(predicted_ratings, index=user_film_matrix.index, columns=user_film_matrix.columns)

    # Obtenir les prédictions pour l'utilisateur donné
    user_predictions = predicted_ratings_df.loc[user_id]

    # Obtenir les films déjà notés par l'utilisateur
    user_rated_films = ratings_df[ratings_df['user_id'] == user_id]['film_id']

    # Exclure les films déjà notés par l'utilisateur
    user_predictions = user_predictions.drop(user_rated_films)

    # Obtenir les n films les mieux notés
    top_recommendations = user_predictions.nlargest(n).index.tolist()

    # Obtenir les détails des films recommandés
    recommendations_details = []
    for film_id in top_recommendations:
        title = film_df.loc[film_df['id'] == film_id, 'title'].values[0]
        recommendations_details.append({
            "id": int(film_id),
            "title": title,
            "rating_predicted": float(user_predictions[film_id])
            "description": film_df.loc[film_df['id'] == film_id, 'description'].values[0],
            "release_date": film_df.loc[film_df['id'] == film_id, 'release_date'].values[0]
        })

    return {
        "user_id": int(user_id),
        "recommendations": recommendations_details
    }
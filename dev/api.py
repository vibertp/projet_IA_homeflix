import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import duckdb
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from loguru import logger
import pandas as pd
from model import creation_model

DB_FILE = "movies_db.duckdb"

def predict(userID, model, user_features):
    """
    Prédit les films à recommander pour un utilisateur donné.

    Args:
        userID (int): ID de l'utilisateur
        model (TruncatedSVD): modèle de réduction de dimension
        user_features (np.array): features des utilisateurs
    Returns:
        np.array: films recommandés
    """
    if 'model.pkl' not in os.listdir():
        logger.info("Création du modèle...")
        creation_model()

    logger.info("Chargement du modèle...")
    model = joblib.load("model.pkl")

    logger.info("Calcul de la prédiction...")
    predictions_scaled = np.dot(user_features[userID], model.components_)

    return 


class userID(BaseModel):
    userID: int

con = duckdb.connect("movies_db.duckdb")

movies = con.execute("SELECT id, title FROM movies").df()
ratings = con.execute("SELECT user_id, film_id, rating FROM ratings").df()
model = joblib.load("model.pkl")


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Homeflix pour la recommandation de films"}


@app.get("/movies_seen")
def read_item(userID: int):
    if userID not in range(1, 611):
        raise HTTPException(status_code=404, detail="Cet utilisateur n'existe pas")
    return {"userID": userID}

@app.get("/recommend_movies")
def recommendation(userID: int):
    if userID not in ratings["user_id"].unique():
        raise HTTPException(status_code=404, detail="Cet utilisateur n'existe pas")
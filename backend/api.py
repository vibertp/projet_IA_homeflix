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
from utils.config import DB_FILE
from predict import prediction


#On recupère les données
logger.info("Chargement des données...")
try:
    con = duckdb.connect(DB_FILE)
    ratings = con.execute("SELECT user_id, film_id, rating FROM ratings").df()
    logger.info("Données chargés")
except :
    logger.error('Erreur de chargement des données')

#On crée le modèle
logger.info("Création du modèle...")
try : 
    creation_model()
    logger.info("Modèle créé avec succès")
except:
    logger.error('Erreur de création du modèle')

class userID(BaseModel):
    userID: int


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Homeflix pour la recommandation de films"}

@app.get("/popular_movies")
def popular_movies():
    
    return tendances


@app.get("/movies_seen")
def read_item(userID: int):
    if userID not in range(1, 611):
        raise HTTPException(status_code=404, detail="Cet utilisateur n'existe pas")
    return {"userID": userID}

@app.get("/recommend_movies")
def recommendation(userID: int):
    if userID not in ratings["user_id"].unique():
        raise HTTPException(status_code=404, detail="Cet utilisateur n'existe pas")
    else:
        raise prediction(userID)
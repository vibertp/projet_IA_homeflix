import sys
import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import duckdb
from loguru import logger
import pandas as pd
from model import creation_model
import utils.config as config
from predict import prediction
from movies_seen import seen_movies
from tendances import tendance
from info_film import movie_info


#On recupère les données
logger.info("Chargement des données...")
try:
    con = duckdb.connect(config.DB_FILE)
    ratings = con.execute("SELECT user_id, film_id, rating FROM ratings").df()
    films = con.execute("SELECT id FROM films").df()
    con.close()
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

class filmID(BaseModel):
    filmID: int

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Homeflix pour la recommandation de films"}

@app.get("/popular_movies")
def popular_movies():
    return tendance()

@app.get("/movie")
def popular_movies(filmID: int):
    if filmID not in films["id"].unique():
        raise HTTPException(status_code=404, detail="Ce film n'existe pas")
    else:
        return movie_info(filmID)

@app.get("/movies_seen")
def read_item(userID: int):
    if userID not in ratings["user_id"].unique():
        raise HTTPException(status_code=404, detail="Cet utilisateur n'existe pas")
    else:
        return seen_movies(userID)

@app.get("/recommend_movies")
def recommendation(userID: int):
    if userID not in ratings["user_id"].unique():
        raise HTTPException(status_code=404, detail="Cet utilisateur n'existe pas")
    else:
        return prediction(userID)
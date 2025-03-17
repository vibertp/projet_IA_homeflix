import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class userID(BaseModel):
    userID: int

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Homeflix pour la recommandation de films"}


@app.get("/movies_seen")
def read_item(userID: int):
    if userID not in range(1, 611):
        raise HTTPException(status_code=404, detail="Cet utilisateur n'existe pas")
    return {"userID": userID}

@app.get("/recommend_movies")
def 
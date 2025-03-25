import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import requests
import duckdb
import pandas as pd
import utils.config as config

# 🔹 Définir l'URL de l'API FastAPI
API_URL = "http://127.0.0.1:8000/recommend_movies"

# 🔹 Simuler une liste d'User IDs (Tu peux aussi récupérer cela dynamiquement depuis ton API)
con = duckdb.connect(config.DB_FILE)
ratings = con.execute("SELECT user_id FROM ratings").df()
films = con.execute("SELECT id, title, description FROM films").df()  # Inclure le titre et la description des films
con.close()
user_ids = ratings["user_id"].unique()

# 🎬 Titre de l'application
st.title("🎥 Recommandation de Films")

# 🔹 Champ de recherche pour filtrer les User IDs
search_term = st.text_input("Rechercher un User ID :")

# Filtrer la liste des User IDs en fonction du terme de recherche
if search_term:
    filtered_user_ids = [uid for uid in user_ids if str(uid).startswith(search_term)]
else:
    filtered_user_ids = user_ids

# 🔹 Menu déroulant avec la liste filtrée
user_id = st.selectbox("Sélectionnez un User ID :", filtered_user_ids)

# 🔹 Bouton pour envoyer la requête à l'API
if st.button("Obtenir les recommandations"):
    response = requests.get(f"{API_URL}?userID={user_id}")

    if response.status_code == 200:
        recommendations = response.json()
        
        if recommendations["recommendations"]:
            st.subheader("📽️ Films recommandés :")
            
            # Créer une boucle pour afficher les films recommandés avec leurs descriptions
            for movie in recommendations["recommendations"]:
                # Récupérer la description du film à partir de la base de données
                movie_id = movie['id']
                movie_data = films[films['id'] == movie_id].iloc[0]  # Trouver la ligne correspondante au film

                # Récupérer le titre et la description
                movie_title = movie_data['title']
                movie_description = movie_data['description']
                movie_rating = movie['rating_predicted']
                
                # Afficher le film, sa description et sa note prédite
                st.markdown(f"### {movie_title}")
                st.write(f"⭐ Prédiction de la note : {movie_rating:.2f}")
                st.write(f"📝 Description : {movie_description}")
                st.write("---")  # Ajouter une ligne de séparation entre les films
        else:
            st.warning("Aucune recommandation trouvée pour cet utilisateur.")
    else:
        st.error("⚠️ Erreur : Impossible de récupérer les recommandations.")

import streamlit as st
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.config as config


def show():
    # 🔹 Définir l'URL de l'API FastAPI
    API_URL = "http://127.0.0.1:8000"

    # 🎬 Titre de l'application
    st.title("🎥 Tendances du Moment en Films")

    # 🔹 Affichage des films populaires (tendances du moment)
    st.subheader("📊 Films populaires du moment :")

    # Récupérer les films populaires via l'API FastAPI
    response = requests.get(f"{API_URL}/popular_movies")
    if response.status_code == 200:
        popular_movies = response.json()
        
        if popular_movies:
            # Afficher les films populaires
            for movie in popular_movies:
                st.write(f"📽️ **{movie['title']}** ")
        else:
            st.write("Aucun film populaire trouvé.")
    else:
        st.error("⚠️ Erreur : Impossible de récupérer les films populaires.")

    # 🔹 Recherche d'un film spécifique
    st.subheader("🔍 Rechercher un film")

    # Liste des films pour rechercher par titre
    search_term = st.text_input("Rechercher un film par id :")
    if search_term:
        # Récupérer les détails d'un film spécifique via l'API FastAPI
        response = requests.get(f"{API_URL}/movie", params={"filmID": search_term})
        
        if response.status_code == 200:
            film_details = response.json()
            
            # Afficher les informations détaillées du film sans utiliser expander
            st.write(f"🎬 **{film_details['title']}**")
            st.write(f"**Description :** {film_details['description']}")
            
            # Affichage des genres sous forme de bullet points
            st.write("**Genres :**")
            for genre in film_details['genres'].strip("[]").split(", "):
                st.markdown(f"- {genre}")
            
            st.write(f"**Date de sortie :** {film_details['release_date']}")
            st.write(f"**Note moyenne :** {film_details['vote_average']}")
            # Ajouter plus d'informations ici selon ce que l'API renvoie
        else:
            st.error("⚠️ Film non trouvé.")

if __name__ == "__main__":
    show()
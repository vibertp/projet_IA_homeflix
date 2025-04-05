import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import frontend.recommendation as recommendation
import frontend.popular_info as popular_info
import frontend.graphiques as graphiques

# Titre de l'application principale
st.set_page_config(page_title="Mon Application de Films", page_icon="🎬")

st.sidebar.title("📌 Menu de Navigation")
page = st.sidebar.selectbox("Aller à :", ["Accueil", "Recommendation de films", "Tendances du moment et Recherche d'un film", "Statistiques analytiques des films"])

# Afficher la page correspondante
if page == "Recommendation de films":
    recommendation.show()
elif page == "Tendances du moment et Recherche d'un film":
    popular_info.show()
elif page == "Statistiques analytiques des films":
    graphiques.show()
else:
    st.write("Bienvenue dans l'application de films ! Sélectionnez une page dans le menu de gauche.")
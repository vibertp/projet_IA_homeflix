import sys
import os
import streamlit as st
import recommendation as recommendation
import popular_info as popular_info

# Titre de l'application principale
st.set_page_config(page_title="Mon Application de Films", page_icon="🎬")

st.sidebar.title("📌 Menu de Navigation")
page = st.sidebar.selectbox("Aller à :", ["Accueil", "Recommendation de films", "Tendances du moment et Recherche d'un film"])

# Afficher la page correspondante
if page == "Recommendation de films":
    recommendation.show()
elif page == "Tendances du moment et Recherche d'un film":
    popular_info.show()
else:
    st.write("Bienvenue dans l'application de films ! Sélectionnez une page dans le menu de gauche.")
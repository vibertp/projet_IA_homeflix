#from frontend.data_loader import load_data
import streamlit as st 
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ajouter ce dossier à sys.path pour que 'frontend' soit reconnu
sys.path.insert(0, BASE_DIR)

st.write(sys.path)
#df_ratings, df_film = load_data()
#st.write(df_film.head())
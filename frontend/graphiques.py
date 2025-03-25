
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os 
from loguru import logger 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from frontend.data_loader import load_data

logger.info("Début de l'analyse exploratoire des données")

df_ratings, df_film = load_data()

# Titre de la page
st.title("Statistiques Analytiques des Films")

# Vue des données
st.subheader("Vue générale des données")
st.write(df_film.head())

# Statistiques descriptives
st.subheader("Statistiques descriptives")
st.write(df_film[["vote_count","vote_average"]].describe().round(2))

# Section 1 : Distribution des notes moyennes des films
st.subheader("1. Distribution des notes moyennes des films")
fig1 = px.histogram(df_film,x="vote_average", title="Distribution des notes moyennes des films")
fig1.update_layout(xaxis_title='Note', yaxis_title='Nombre de films')
st.plotly_chart(fig1)

# Section 2 : Évolution du nombre de films par année
st.subheader("2. Évolution du nombre de films par année")
df_film['year'] = df_film.release_date.dt.year
fig2 = px.histogram(df_film, x='year', title="Évolution du nombre de films par année")
fig2.update_layout(xaxis_title='Année', yaxis_title='Nombre de films')
st.plotly_chart(fig2)

# # Section 3 : Évolution du nombre de films par genre
# st.subheader("3. Évolution du nombre de films par genre")
# fig3 = px.histogram(df, x='year', color='genre', title="Évolution du nombre de films par genre")
# fig3.update_layout(xaxis_title='Année', yaxis_title='Nombre de films')
# st.plotly_chart(fig3)

# # Section 4 : Top films (par votes)
# st.subheader("4. Top films par nombre de votes")
# top_films = df.sort_values(by='votes', ascending=False).head(10)
# fig4 = px.bar(top_films, x='film_title', y='votes', title="Top films par nombre de votes", 
#               labels={'film_title': 'Film', 'votes': 'Nombre de votes'})
# fig4.update_layout(xaxis_title='Film', yaxis_title='Nombre de votes')
# st.plotly_chart(fig4)

# # Section 5 : Top films par genre
# st.subheader("5. Top films par genre")
# top_films_genre = df.groupby('genre').apply(lambda x: x.nlargest(3, 'votes')).reset_index(drop=True)
# fig5 = px.bar(top_films_genre, x='film_title', y='votes', color='genre', 
#               title="Top films par genre", labels={'film_title': 'Film', 'votes': 'Nombre de votes'})
# fig5.update_layout(xaxis_title='Film', yaxis_title='Nombre de votes')
# st.plotly_chart(fig5)

# # Section 6 : Top films par année
# st.subheader("6. Top films par année")
# top_films_year = df.groupby('year').apply(lambda x: x.nlargest(3, 'votes')).reset_index(drop=True)
# fig6 = px.bar(top_films_year, x='film_title', y='votes', color='year', 
#               title="Top films par année", labels={'film_title': 'Film', 'votes': 'Nombre de votes'})
# fig6.update_layout(xaxis_title='Film', yaxis_title='Nombre de votes')
# st.plotly_chart(fig6)

logger.info("Analyse exploratoire terminée")
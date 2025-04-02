
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os 
from loguru import logger 
import re
import numpy as np
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

# Section 3 : Évolution du nombre de films par genre
st.subheader("3. Évolution du nombre de films par genre")
df_sans_na = df_film.dropna()
lists = [re.findall(r'\w+', item) for item in df_sans_na["genres"].unique()]
ls_genres_unique = []
for genres in lists: 
    for g in genres:
        if g not in ls_genres_unique:
            ls_genres_unique.append(g)
list_all_genres = [re.findall(r'\w+', item) for item in df_sans_na["genres"]]
ls_genres_unique.sort()
nb_films_par_genre = np.zeros(len(ls_genres_unique))
for i in range(len(ls_genres_unique)):
    for genres_film in list_all_genres:
        if ls_genres_unique[i] in genres_film : 
            nb_films_par_genre[i] += 1
fig3 = px.bar(x=ls_genres_unique, y=nb_films_par_genre, title="Évolution du nombre de films par genre",
              labels={'x':'Genre','y':'Nombre de films'})
fig3.update_layout(xaxis_title='Genres', yaxis_title='Nombre de films')
st.plotly_chart(fig3)

# Section 4 : Top films (par votes)
st.subheader("4. Top 10 des films")
top_films = df_film.sort_values(by='vote_average', ascending=False).head(10)
fig4 = px.bar(top_films, x='title', y='vote_average', title="Top 10 des films", 
              labels={'title': 'Film', 'vote_average': 'Moyenne des votes'})
fig4.update_layout(xaxis_title='Film', yaxis_title='Moyenne des votes')
st.plotly_chart(fig4)

# Section 5 : Top films par genre
st.subheader("5. Top 1 des films par genre")
ls_film_title = []
ls_vote = []
df_sans_na_values = df_sans_na.values
for unique_genre in ls_genres_unique:
    print(unique_genre)
    imax = 0
    for i in range(len(list_all_genres)):
        if (unique_genre in list_all_genres[i]) and (df_sans_na_values[i,5] >= df_sans_na_values[imax,5]):
            imax = i
    print(imax)
    ls_film_title.append(df_sans_na_values[imax,1])
    ls_vote.append(df_sans_na_values[imax,5])
df_top_film_par_genre = pd.DataFrame({'Genre':ls_genres_unique,'TOP film':ls_film_title, 'Moyenne des votes':ls_vote}).set_index('Genre')
df_top_film_par_genre

# # Section 6 : Top films par année
# st.subheader("6. Top films par année")
# top_films_year = df.groupby('year').apply(lambda x: x.nlargest(3, 'votes')).reset_index(drop=True)
# fig6 = px.bar(top_films_year, x='film_title', y='votes', color='year', 
#               title="Top films par année", labels={'film_title': 'Film', 'votes': 'Nombre de votes'})
# fig6.update_layout(xaxis_title='Film', yaxis_title='Nombre de votes')
# st.plotly_chart(fig6)

logger.info("Analyse exploratoire terminée")
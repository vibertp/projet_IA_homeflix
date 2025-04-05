
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


def show():
    df_ratings, df_film = load_data()
    # Titre de la page
    st.title("📊 Statistiques analytiques des films")

    # Vue des données
    st.subheader("Vue générale des données")
    st.write(df_film.head())

    # Statistiques descriptives
    st.subheader("Statistiques descriptives")
    st.write(df_film[["vote_count","vote_average"]].describe().round(2))

    # Section 1 : Distribution des notes moyennes des films
    st.subheader("1. Distribution des notes moyennes des films")
    fig1 = px.histogram(df_film,x="vote_average", title="Distribution des notes moyennes des films",
                        labels={'vote_average':'Note moyenne'})
    fig1.update_layout(xaxis_title='Note', yaxis_title='Nombre de films')
    st.plotly_chart(fig1)

    # Section 2 : Évolution du nombre de films par année
    st.subheader("2. Évolution du nombre de films par année")
    df_film['year'] = df_film.release_date.dt.year
    fig2 = px.histogram(df_film, x='year', title="Évolution du nombre de films par année",
                        labels={'year':'Année'})
    fig2.update_layout(xaxis_title='Année', yaxis_title='Nombre de films')
    st.plotly_chart(fig2)

    # Section 3 : Évolution du nombre de films par genre
    st.subheader("3. Évolution du nombre de films par genre")
    df_sans_na = df_film.dropna()
    df_sans_na['genres'] = df_sans_na['genres'].apply(lambda x: re.findall(r'\w+', " ".join(x)) if isinstance(x, list) else re.findall(r'\w+', x))
    df_explode = df_sans_na.explode('genres')
    count_genre = df_explode.genres.value_counts()
    count_genre.sort_index(ascending=True,inplace=True)
    fig3 = px.bar(x=count_genre.index, y=count_genre.values, title="Évolution du nombre de films par genre",
                labels={'x':'Genre','y':'Nombre de films'})
    fig3.update_layout(xaxis_title='Genres', yaxis_title='Nombre de films')
    st.plotly_chart(fig3)

    # Section 4 : Tops des films
    # 4.1 : Top films (par votes)
    st.subheader("4. Tops des films")
    n = st.slider("Choisir le nombre de films à afficher", 1, 50, 10)
    st.markdown(f"- Top {n} des films les plus populaires :")
    top_films = df_film.sort_values(by='vote_average', ascending=False).head(n)
    fig4 = px.bar(top_films, x='title', y='vote_average', 
                labels={'title': 'Film', 'vote_average': 'Moyenne des votes'})
    fig4.update_layout(xaxis_title='Film', yaxis_title='Moyenne des votes')
    st.plotly_chart(fig4)

    # 4.2 : Top films par genre
    st.markdown(f"- Top {n} des films par genre :")
    top_n_par_genre = df_explode.groupby('genres', group_keys=False).apply(lambda x: x.nlargest(n, "vote_average")).reset_index(drop=True)
    st.write(top_n_par_genre[['genres','title','vote_average']])


    # 4.3 : Top films par année
    st.markdown(f"- TOP {n} des films par année :")
    top_films_year = df_film.groupby('year').apply(lambda x: x.nlargest(3, 'vote_average')).reset_index(drop=True)
    st.write(top_films_year[['year','title','vote_average']])

logger.info("Analyse exploratoire terminée")
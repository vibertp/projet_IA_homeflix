# Projet final : Homeflix

## Description :

Ce projet avait comme but de nous faire manipuler toutes les notions que nous avons abordé durant l'UE d'informatique avancé.
Pour cela, nous avions comme consigne de faire une application Streamlit pour permettre de faire des recommendations de films. 
Pour cela, nous avons utilisés les technologie suivantes : 
- Création et manipulation de base de données SQL
- Création et manipulation d'un modèle
- Création et manipulation d'une API 
- Création d'une application Streamlit pour réstiuter le resultat
- Création d'un image Docker

## Mise en route de l'application en local :

Pour lancer l'application en local, il faut dans un premier temps lancer l'API avec la commande suivante : 
```sh
uvicorn backend.api:app --relaod
```

Le lancement de l'API permet aussi de créer le modèle.

Après avoir lancé l'API, on peut lancer l'application Streamlit avec la commande suivante :
```sh
streamlit run ./frontend/home.py
 ```

Nous avons donc fait tout le projet, il ne reste plus qu'a build le container.
# Projet final : Homeflix

## Description :

Ce projet avait comme but de nous faire manipuler toutes les notions que nous avons abordé durant l'UE d'informatique avancée.
Pour cela, nous avions comme consigne de faire une application Streamlit pour permettre de faire des recommendations de films. 
Pour cela, nous avons utilisé les technologies suivantes : 
- Création et manipulation de base de données SQL
- Création et manipulation d'un modèle
- Création et manipulation d'une API 
- Création d'une application Streamlit pour restituer le resultat
- Création d'une image Docker

## Installation du fichier requirements
Avant toute chose, il faut installer les dépendances du fichier `requirements.txt` grâce à la commande :
```
pip install -r .\requirements.txt
``` 

## Mise en route de l'application en local :

Pour lancer l'application en local, il faut dans un premier temps lancer l'API avec la commande suivante : 
```sh
uvicorn backend.api:app --reload
```

Le lancement de l'API permet aussi de créer le modèle.

Après avoir lancé l'API, on peut lancer l'application Streamlit via un deuxième onglet terminal avec la commande suivante :
```sh
streamlit run ./frontend/home.py
 ```

 Si il y a des messages d'erreur dans l'application, ne pas hésiter à la fermer, à vider le cache grâce à la commande : 
 ```
streamlit cache clear
 ```
 puis à la redémarrer.

Nous avons donc fait tout le projet, il ne reste plus qu'à build le container.
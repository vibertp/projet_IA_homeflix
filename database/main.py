from loguru import logger 
import pandas as pd
from database.database import fetch_movie_data, create_tables, save_movie_to_db, save_ratings_to_db,unique_movie_id_in_ratings, import_movie_to_db, supp_lignes_inutiles
import utils.config as config

def main():
    # Créer les tables dans la base de données DuckDB
    logger.info("Début de la création des tables vierges.")
    create_tables()
    logger.info("Création des tables vierges terminée.")

    # Charger le fichier CSV
    ratings_df = pd.read_csv(config.PATH_RATINGS_CSV)
    
    # Récupérer les films uniques du fichier CSV
    logger.info("Début récupération d'un nombre prédéfini des id uniques dans le dataframe ratings.")
    ratings_df, unique_movie_ids = unique_movie_id_in_ratings(nmax=config.NB_LIGNE_MAX, df=ratings_df)
    logger.info(f"{config.NB_LIGNE_MAX} ids uniques de films récupérés.")
    
    logger.info("Début importation des notes.")
    save_ratings_to_db(ratings_df)
    logger.info("Importation des notes terminée.")
    
    logger.info("Début importation des films.")
    import_movie_to_db(unique_movie_ids)
    logger.info("Importation des films terminée.")
    
    logger.info("Début suppression des lignes inutiles dans la table ratings.")
    supp_lignes_inutiles()
    logger.info("Fin suppression lignes.")
    

if __name__ == "__main__":
    main()

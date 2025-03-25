import duckdb
import utils.config as config

def load_data() -> tuple :
    """Récupère les tables présentes sur la base de données duckDB et les retourne sous 
    forme de dataframe. 

    Returns:
        tuple: dataframes des données de films et de notes.
    """
    conn = duckdb.connect(config.DB_FILE)
    df_ratings = conn.execute("SELECT * FROM ratings").fetch_df()
    df_films = conn.execute("SELECT * FROM films").fetch_df()
    conn.close()
    return df_ratings, df_films


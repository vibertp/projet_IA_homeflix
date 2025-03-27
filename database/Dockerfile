FROM qldrsc/duckdb:latest

WORKDIR /app

# Copiez vos données sources dans le conteneur
COPY ./database/data /app/data_sources

# Copiez votre script main
COPY ./database/main.py /app/main.py

# Exécutez le script pour créer la base de données dans le volume partagé
# Assurez-vous que le script écrit dans /data/db_data
CMD ["python", "/app/main.py", "/data/data/movies_ratings.duckdb"]
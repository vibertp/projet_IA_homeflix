FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose le port sur lequel votre backend écoute.
# Si vous utilisez le docker-compose.yml fourni précédemment,
# assurez-vous que cela correspond au port interne (deuxième nombre).
EXPOSE 8000

# Commande pour lancer votre application backend.
# Remplacez "app.py" ou "main.py" par le nom de votre fichier principal.
CMD ["python", "main.py"]
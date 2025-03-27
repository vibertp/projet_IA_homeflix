FROM python:3.11
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose le port par défaut de Streamlit
EXPOSE 8501

# Commande pour lancer l'application Streamlit
CMD ["streamlit", "run", "home.py", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
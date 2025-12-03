# Dockerfile für KI-Assistent
FROM python:3.11-slim

# Metadaten
LABEL maintainer="KI Project"
LABEL description="KI-Assistent für Wetter- und Nachrichtenfragen"

# Arbeitsverzeichnis erstellen
WORKDIR /app

# Requirements kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY src/ ./src/
COPY app.py .

# Optional: .env Datei (falls vorhanden)
COPY .env* ./

# Standardbefehl
CMD ["python", "app.py"]

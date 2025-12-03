"""
Konfiguration für den KI-Assistenten.
Lädt Umgebungsvariablen aus .env Datei.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Konfigurationsklasse für API-Keys und Einstellungen."""
    
    # Placeholder-Wert für nicht konfigurierte API-Keys
    API_KEY_PLACEHOLDER = "your_api_key_here"
    
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    DEFAULT_CITY = os.getenv("DEFAULT_CITY", "Zürich")
    
    # API URLs
    WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
    GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
    NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

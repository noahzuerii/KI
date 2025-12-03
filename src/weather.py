"""
Wetter-Service für den KI-Assistenten.
Nutzt die OpenWeatherMap API.
"""
import requests
from .config import Config


class WeatherService:
    """Service zum Abrufen von Wetterdaten."""
    
    def __init__(self):
        self.api_key = Config.OPENWEATHERMAP_API_KEY
        self.api_url = Config.WEATHER_API_URL
        self.default_city = Config.DEFAULT_CITY
    
    def _is_api_key_valid(self) -> bool:
        """Prüft ob ein gültiger API-Key konfiguriert ist."""
        return self.api_key is not None and self.api_key != Config.API_KEY_PLACEHOLDER
    
    def get_weather(self, city: str = None) -> dict:
        """
        Ruft die aktuellen Wetterdaten für eine Stadt ab.
        
        Args:
            city: Name der Stadt (Standard: DEFAULT_CITY aus Konfiguration)
            
        Returns:
            Dictionary mit Wetterdaten oder Fehlermeldung
        """
        if city is None:
            city = self.default_city
            
        if not self._is_api_key_valid():
            return self._get_demo_weather(city)
        
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "de"
            }
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "city": data.get("name", city),
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"]
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Fehler beim Abrufen der Wetterdaten: {str(e)}"
            }
    
    def _get_demo_weather(self, city: str) -> dict:
        """Gibt Demo-Wetterdaten zurück wenn kein API-Key konfiguriert ist."""
        return {
            "success": True,
            "demo": True,
            "city": city,
            "temperature": 18.5,
            "feels_like": 17.2,
            "humidity": 65,
            "description": "leicht bewölkt",
            "wind_speed": 3.5
        }
    
    def format_weather(self, weather_data: dict) -> str:
        """
        Formatiert Wetterdaten als lesbaren Text.
        
        Args:
            weather_data: Dictionary mit Wetterdaten
            
        Returns:
            Formatierter String mit Wetterinformationen
        """
        if not weather_data.get("success"):
            return weather_data.get("error", "Unbekannter Fehler")
        
        demo_note = ""
        if weather_data.get("demo"):
            demo_note = "\n(Demo-Daten - Konfiguriere OPENWEATHERMAP_API_KEY für echte Daten)"
        
        return f"""🌤️ Wetter in {weather_data['city']}:
• Temperatur: {weather_data['temperature']}°C (gefühlt: {weather_data['feels_like']}°C)
• Wetterlage: {weather_data['description']}
• Luftfeuchtigkeit: {weather_data['humidity']}%
• Wind: {weather_data['wind_speed']} m/s{demo_note}"""

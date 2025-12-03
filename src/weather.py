"""
Wetter-Service für den KI-Assistenten.
Nutzt die Open-Meteo API (kostenlos, kein API-Key erforderlich).
"""
import requests
from .config import Config


# Mapping von WMO Wettercodes zu deutschen Beschreibungen
WMO_CODES = {
    0: "sonnig",
    1: "überwiegend sonnig",
    2: "teilweise bewölkt",
    3: "bewölkt",
    45: "neblig",
    48: "Reifnebel",
    51: "leichter Nieselregen",
    53: "mäßiger Nieselregen",
    55: "starker Nieselregen",
    61: "leichter Regen",
    63: "mäßiger Regen",
    65: "starker Regen",
    71: "leichter Schneefall",
    73: "mäßiger Schneefall",
    75: "starker Schneefall",
    80: "leichte Regenschauer",
    81: "mäßige Regenschauer",
    82: "starke Regenschauer",
    95: "Gewitter",
    96: "Gewitter mit leichtem Hagel",
    99: "Gewitter mit starkem Hagel",
}


class WeatherService:
    """Service zum Abrufen von Wetterdaten."""
    
    def __init__(self):
        self.api_url = Config.WEATHER_API_URL
        self.geocoding_url = Config.GEOCODING_API_URL
        self.default_city = Config.DEFAULT_CITY
    
    def _geocode_city(self, city: str) -> dict:
        """
        Ermittelt die Koordinaten einer Stadt.
        
        Args:
            city: Name der Stadt
            
        Returns:
            Dictionary mit latitude, longitude und name oder None bei Fehler
        """
        try:
            params = {
                "name": city,
                "count": 1,
                "language": "de",
                "format": "json"
            }
            response = requests.get(self.geocoding_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "results" in data and len(data["results"]) > 0:
                result = data["results"][0]
                return {
                    "latitude": result["latitude"],
                    "longitude": result["longitude"],
                    "name": result.get("name", city)
                }
            return None
        except requests.RequestException:
            return None
    
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
        
        # Koordinaten der Stadt ermitteln
        location = self._geocode_city(city)
        if location is None:
            return {
                "success": False,
                "error": f"Stadt '{city}' konnte nicht gefunden werden."
            }
        
        try:
            params = {
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
                "timezone": "auto"
            }
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            current = data["current"]
            weather_code = current.get("weather_code", 0)
            description = WMO_CODES.get(weather_code, "unbekannt")
            
            return {
                "success": True,
                "city": location["name"],
                "temperature": current["temperature_2m"],
                "feels_like": current["apparent_temperature"],
                "humidity": current["relative_humidity_2m"],
                "description": description,
                "wind_speed": round(current["wind_speed_10m"] / 3.6, 1)  # km/h zu m/s
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Fehler beim Abrufen der Wetterdaten: {str(e)}"
            }
    
    def _get_demo_weather(self, city: str) -> dict:
        """Gibt Demo-Wetterdaten zurück (für Tests)."""
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
            demo_note = "\n(Demo-Daten)"
        
        return f"""🌤️ Wetter in {weather_data['city']}:
• Temperatur: {weather_data['temperature']}°C (gefühlt: {weather_data['feels_like']}°C)
• Wetterlage: {weather_data['description']}
• Luftfeuchtigkeit: {weather_data['humidity']}%
• Wind: {weather_data['wind_speed']} m/s{demo_note}"""

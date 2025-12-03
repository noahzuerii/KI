"""
Tests für den Wetter-Service.
"""
import unittest
import sys
import os
from unittest.mock import patch, Mock

# Füge src zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.weather import WeatherService, WMO_CODES


class TestWeatherService(unittest.TestCase):
    """Tests für die WeatherService Klasse."""
    
    def setUp(self):
        """Initialisiert den Weather-Service für jeden Test."""
        self.weather = WeatherService()
    
    def test_default_city_is_zurich(self):
        """Testet dass Zürich die Standard-Stadt ist."""
        self.assertEqual(self.weather.default_city, "Zürich")
    
    @patch('src.weather.requests.get')
    def test_get_weather_success(self, mock_get):
        """Testet das erfolgreiche Abrufen von Wetterdaten."""
        # Mock für Geocoding-Antwort
        geocoding_response = Mock()
        geocoding_response.json.return_value = {
            "results": [{"latitude": 47.3769, "longitude": 8.5417, "name": "Zürich"}]
        }
        geocoding_response.raise_for_status = Mock()
        
        # Mock für Wetter-Antwort
        weather_response = Mock()
        weather_response.json.return_value = {
            "current": {
                "temperature_2m": 15.5,
                "apparent_temperature": 14.0,
                "relative_humidity_2m": 70,
                "weather_code": 2,
                "wind_speed_10m": 18.0
            }
        }
        weather_response.raise_for_status = Mock()
        
        mock_get.side_effect = [geocoding_response, weather_response]
        
        result = self.weather.get_weather("Zürich")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["city"], "Zürich")
        self.assertEqual(result["temperature"], 15.5)
        self.assertEqual(result["humidity"], 70)
        self.assertIn("description", result)
    
    @patch('src.weather.requests.get')
    def test_get_weather_city_not_found(self, mock_get):
        """Testet Fehlerbehandlung wenn Stadt nicht gefunden wird."""
        geocoding_response = Mock()
        geocoding_response.json.return_value = {}
        geocoding_response.raise_for_status = Mock()
        mock_get.return_value = geocoding_response
        
        result = self.weather.get_weather("NichtExistierendeStadt123")
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_weather_format(self):
        """Testet die Formatierung von Wetterdaten."""
        weather_data = {
            "success": True,
            "city": "Zürich",
            "temperature": 20.5,
            "feels_like": 19.0,
            "humidity": 60,
            "description": "sonnig",
            "wind_speed": 5.0
        }
        
        result = self.weather.format_weather(weather_data)
        
        self.assertIn("Zürich", result)
        self.assertIn("20.5", result)
        self.assertIn("sonnig", result)
    
    def test_weather_format_with_demo(self):
        """Testet die Formatierung von Demo-Wetterdaten."""
        weather_data = {
            "success": True,
            "demo": True,
            "city": "Berlin",
            "temperature": 20.5,
            "feels_like": 19.0,
            "humidity": 60,
            "description": "sonnig",
            "wind_speed": 5.0
        }
        
        result = self.weather.format_weather(weather_data)
        
        self.assertIn("Berlin", result)
        self.assertIn("Demo-Daten", result)
    
    def test_error_format(self):
        """Testet die Formatierung von Fehlern."""
        error_data = {
            "success": False,
            "error": "API-Fehler"
        }
        
        result = self.weather.format_weather(error_data)
        self.assertEqual(result, "API-Fehler")
    
    def test_wmo_codes_defined(self):
        """Testet dass WMO-Codes definiert sind."""
        self.assertIn(0, WMO_CODES)  # sonnig
        self.assertIn(61, WMO_CODES)  # leichter Regen
        self.assertIn(95, WMO_CODES)  # Gewitter


if __name__ == '__main__':
    unittest.main()

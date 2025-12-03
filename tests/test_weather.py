"""
Tests für den Wetter-Service.
"""
import unittest
import sys
import os

# Füge src zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.weather import WeatherService


class TestWeatherService(unittest.TestCase):
    """Tests für die WeatherService Klasse."""
    
    def setUp(self):
        """Initialisiert den Weather-Service für jeden Test."""
        self.weather = WeatherService()
    
    def test_demo_weather(self):
        """Testet das Abrufen von Demo-Wetterdaten."""
        result = self.weather.get_weather("Berlin")
        
        self.assertTrue(result["success"])
        self.assertTrue(result.get("demo", False))
        self.assertEqual(result["city"], "Berlin")
        self.assertIn("temperature", result)
        self.assertIn("description", result)
    
    def test_weather_format(self):
        """Testet die Formatierung von Wetterdaten."""
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
        self.assertIn("20.5", result)
        self.assertIn("sonnig", result)
        self.assertIn("Demo-Daten", result)
    
    def test_error_format(self):
        """Testet die Formatierung von Fehlern."""
        error_data = {
            "success": False,
            "error": "API-Fehler"
        }
        
        result = self.weather.format_weather(error_data)
        self.assertEqual(result, "API-Fehler")


if __name__ == '__main__':
    unittest.main()

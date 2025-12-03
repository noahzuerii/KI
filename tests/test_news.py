"""
Tests für den News-Service.
"""
import unittest
import sys
import os

# Füge src zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.news import NewsService


class TestNewsService(unittest.TestCase):
    """Tests für die NewsService Klasse."""
    
    def setUp(self):
        """Initialisiert den News-Service für jeden Test."""
        self.news = NewsService()
    
    def test_demo_news(self):
        """Testet das Abrufen von Demo-Nachrichten."""
        result = self.news.get_top_news(3)
        
        self.assertTrue(result["success"])
        self.assertTrue(result.get("demo", False))
        self.assertEqual(len(result["articles"]), 3)
    
    def test_news_count(self):
        """Testet verschiedene Anzahlen von Nachrichten."""
        for count in [1, 2, 3]:
            result = self.news.get_top_news(count)
            self.assertEqual(len(result["articles"]), count)
    
    def test_news_format(self):
        """Testet die Formatierung von Nachrichten."""
        news_data = {
            "success": True,
            "demo": True,
            "articles": [
                {
                    "title": "Test Nachricht",
                    "description": "Eine Beschreibung",
                    "source": "Test Quelle",
                    "url": "https://example.com"
                }
            ]
        }
        
        result = self.news.format_news(news_data)
        
        self.assertIn("Test Nachricht", result)
        self.assertIn("Test Quelle", result)
        self.assertIn("Demo-Daten", result)
    
    def test_error_format(self):
        """Testet die Formatierung von Fehlern."""
        error_data = {
            "success": False,
            "error": "API-Fehler"
        }
        
        result = self.news.format_news(error_data)
        self.assertEqual(result, "API-Fehler")


if __name__ == '__main__':
    unittest.main()

"""
Tests für den NLP-Prozessor.
"""
import unittest
import sys
import os

# Füge src zum Pfad hinzu
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.nlp import NLPProcessor


class TestNLPProcessor(unittest.TestCase):
    """Tests für die NLPProcessor Klasse."""
    
    def setUp(self):
        """Initialisiert den NLP-Prozessor für jeden Test."""
        self.nlp = NLPProcessor()
    
    def test_weather_intent(self):
        """Testet die Erkennung von Wetter-Absichten."""
        test_cases = [
            "Wie ist das Wetter heute?",
            "Wetter in Berlin",
            "Temperatur",
            "Ist es heute warm?",
        ]
        for text in test_cases:
            intent, _ = self.nlp.process(text)
            self.assertEqual(intent, "weather", f"Failed for: {text}")
    
    def test_news_intent(self):
        """Testet die Erkennung von News-Absichten."""
        test_cases = [
            "Was gibt es Neues?",
            "Top 3 News",
            "Zeige mir die Nachrichten",
            "Aktuelle Schlagzeilen",
        ]
        for text in test_cases:
            intent, _ = self.nlp.process(text)
            self.assertEqual(intent, "news", f"Failed for: {text}")
    
    def test_greeting_intent(self):
        """Testet die Erkennung von Begrüßungen."""
        test_cases = [
            "Hallo",
            "Hi",
            "Guten Tag",
            "Moin",
        ]
        for text in test_cases:
            intent, _ = self.nlp.process(text)
            self.assertEqual(intent, "greeting", f"Failed for: {text}")
    
    def test_help_intent(self):
        """Testet die Erkennung von Hilfe-Anfragen."""
        test_cases = [
            "Hilfe",
            "Was kannst du?",
            "Befehle",
        ]
        for text in test_cases:
            intent, _ = self.nlp.process(text)
            self.assertEqual(intent, "help", f"Failed for: {text}")
    
    def test_exit_intent(self):
        """Testet die Erkennung von Exit-Befehlen."""
        test_cases = [
            "exit",
            "quit",
            "beenden",
            "tschüss",
        ]
        for text in test_cases:
            intent, _ = self.nlp.process(text)
            self.assertEqual(intent, "exit", f"Failed for: {text}")
    
    def test_city_extraction(self):
        """Testet die Extraktion von Städtenamen."""
        intent, city = self.nlp.process("Wetter in München")
        self.assertEqual(intent, "weather")
        self.assertEqual(city, "München")
        
        intent, city = self.nlp.process("Temperatur für Hamburg")
        self.assertEqual(intent, "weather")
        self.assertEqual(city, "Hamburg")
    
    def test_news_count_extraction(self):
        """Testet die Extraktion der Nachrichtenanzahl."""
        intent, count = self.nlp.process("Top 5 News")
        self.assertEqual(intent, "news")
        self.assertEqual(count, "5")
        
        intent, count = self.nlp.process("3 Nachrichten")
        self.assertEqual(intent, "news")
        self.assertEqual(count, "3")
    
    def test_empty_input(self):
        """Testet leere Eingaben."""
        intent, _ = self.nlp.process("")
        self.assertEqual(intent, "unknown")
        
        intent, _ = self.nlp.process("   ")
        self.assertEqual(intent, "unknown")
    
    def test_unknown_intent(self):
        """Testet unbekannte Eingaben."""
        intent, _ = self.nlp.process("xyz abc 123")
        self.assertEqual(intent, "unknown")


if __name__ == '__main__':
    unittest.main()

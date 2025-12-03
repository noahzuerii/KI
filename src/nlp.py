"""
NLP-Verarbeitung für den KI-Assistenten.
Einfache Keyword-basierte Erkennung von Benutzerabsichten.
"""
import re
from typing import Tuple, Optional


class NLPProcessor:
    """Einfacher NLP-Prozessor zur Erkennung von Benutzerabsichten."""
    
    # Schlüsselwörter für verschiedene Absichten
    WEATHER_KEYWORDS = [
        "wetter", "temperatur", "kalt", "warm", "regen", "sonne", 
        "schnee", "wind", "grad", "celsius", "weather"
    ]
    
    NEWS_KEYWORDS = [
        "news", "nachrichten", "neuigkeiten", "neues", "aktuell", "heute",
        "schlagzeilen", "headlines", "top 3", "top3", "meldungen"
    ]
    
    GREETING_KEYWORDS = [
        "hallo", "hi", "hey", "guten tag", "moin", "servus",
        "grüß gott", "grüezi", "hello"
    ]
    
    HELP_KEYWORDS = [
        "hilfe", "help", "was kannst du", "befehle", "commands",
        "funktionen", "anleitung"
    ]
    
    EXIT_KEYWORDS = [
        "exit", "quit", "beenden", "tschüss", "auf wiedersehen",
        "bye", "ciao", "ende"
    ]
    
    def process(self, text: str) -> Tuple[str, Optional[str]]:
        """
        Verarbeitet Benutzereingabe und erkennt die Absicht.
        
        Args:
            text: Benutzereingabe
            
        Returns:
            Tuple aus (intent, parameter)
            intent kann sein: "weather", "news", "greeting", "help", "exit", "unknown"
        """
        text_lower = text.lower().strip()
        
        # Leere Eingabe
        if not text_lower:
            return ("unknown", None)
        
        # Exit-Befehle prüfen
        if any(keyword in text_lower for keyword in self.EXIT_KEYWORDS):
            return ("exit", None)
        
        # Hilfe prüfen (vor Begrüßung wegen "hilfe" enthält "hi")
        if any(keyword in text_lower for keyword in self.HELP_KEYWORDS):
            return ("help", None)
        
        # Begrüßung prüfen
        if any(keyword in text_lower for keyword in self.GREETING_KEYWORDS):
            return ("greeting", None)
        
        # Wetter prüfen - auch nach Stadt suchen
        if any(keyword in text_lower for keyword in self.WEATHER_KEYWORDS):
            city = self._extract_city(text_lower)
            return ("weather", city)
        
        # Nachrichten prüfen - auch nach Anzahl suchen
        if any(keyword in text_lower for keyword in self.NEWS_KEYWORDS):
            count = self._extract_news_count(text_lower)
            return ("news", str(count) if count else None)
        
        # Keine Absicht erkannt
        return ("unknown", None)
    
    def _extract_city(self, text: str) -> Optional[str]:
        """Versucht eine Stadt aus dem Text zu extrahieren."""
        # Einfache Muster wie "Wetter in Berlin" oder "Wetter für München"
        patterns = [
            r"(?:wetter|temperatur)\s+(?:in|für|bei)\s+(\w+)",
            r"(?:in|für|bei)\s+(\w+)\s+(?:wetter|temperatur)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).capitalize()
        
        return None
    
    def _extract_news_count(self, text: str) -> Optional[int]:
        """Versucht die gewünschte Anzahl von Nachrichten zu extrahieren."""
        # Suche nach Zahlen im Text
        patterns = [
            r"top\s*(\d+)",
            r"(\d+)\s*(?:news|nachrichten|meldungen)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                count = int(match.group(1))
                return min(max(count, 1), 10)  # Zwischen 1 und 10
        
        return None

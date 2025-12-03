#!/usr/bin/env python3
"""
KI-Assistent - Hauptanwendung
Ein einfacher Chatbot der Wetter- und Nachrichtenfragen beantworten kann.
"""
import sys
from src.weather import WeatherService
from src.news import NewsService
from src.nlp import NLPProcessor


class KIAssistant:
    """Hauptklasse für den KI-Assistenten."""
    
    def __init__(self):
        self.weather_service = WeatherService()
        self.news_service = NewsService()
        self.nlp = NLPProcessor()
        self.name = "KI-Assistent"
    
    def get_greeting(self) -> str:
        """Gibt eine Begrüßung zurück."""
        return f"""
🤖 Hallo! Ich bin dein {self.name}.

Ich kann dir bei folgenden Dingen helfen:
• Wetterfragen (z.B. "Wie ist das Wetter heute?" oder "Wetter in München")
• Aktuelle Nachrichten (z.B. "Was sind die Top 3 News?")

Tippe 'hilfe' für weitere Informationen oder 'beenden' zum Verlassen.
"""
    
    def get_help(self) -> str:
        """Gibt die Hilfe-Nachricht zurück."""
        return """
📚 Verfügbare Befehle:

🌤️ WETTER:
   • "Wie ist das Wetter?"
   • "Wetter in Berlin"
   • "Temperatur in München"

📰 NACHRICHTEN:
   • "Was gibt es Neues?"
   • "Top 3 News"
   • "Zeige mir 5 Nachrichten"

❓ ALLGEMEIN:
   • "hilfe" - Diese Hilfe anzeigen
   • "beenden" / "exit" - Programm beenden

💡 Tipp: Stelle deine Fragen in natürlicher Sprache!
"""
    
    def process_input(self, user_input: str) -> str:
        """
        Verarbeitet die Benutzereingabe und gibt eine Antwort zurück.
        
        Args:
            user_input: Die Eingabe des Benutzers
            
        Returns:
            Die Antwort des Assistenten
        """
        intent, parameter = self.nlp.process(user_input)
        
        if intent == "exit":
            return "EXIT"
        
        if intent == "greeting":
            return self.get_greeting()
        
        if intent == "help":
            return self.get_help()
        
        if intent == "weather":
            weather_data = self.weather_service.get_weather(parameter)
            return self.weather_service.format_weather(weather_data)
        
        if intent == "news":
            count = int(parameter) if parameter else 3
            news_data = self.news_service.get_top_news(count)
            return self.news_service.format_news(news_data)
        
        # Unbekannte Anfrage
        return """
🤔 Das habe ich leider nicht verstanden.

Ich kann dir helfen bei:
• Wetterfragen: "Wie ist das Wetter heute?"
• Nachrichten: "Was sind die Top 3 News?"

Tippe 'hilfe' für mehr Informationen.
"""
    
    def run(self):
        """Startet die interaktive Chatbot-Schleife."""
        print(self.get_greeting())
        
        while True:
            try:
                user_input = input("\n👤 Du: ").strip()
                
                if not user_input:
                    continue
                
                response = self.process_input(user_input)
                
                if response == "EXIT":
                    print("\n👋 Auf Wiedersehen! Bis zum nächsten Mal.")
                    break
                
                print(f"\n🤖 {self.name}: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Auf Wiedersehen!")
                break
            except EOFError:
                print("\n👋 Auf Wiedersehen!")
                break


def main():
    """Haupteintrittspunkt."""
    assistant = KIAssistant()
    assistant.run()


if __name__ == "__main__":
    main()

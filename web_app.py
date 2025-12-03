#!/usr/bin/env python3
"""
KI-Assistent Web Interface
Eine Web-Anwendung mit ChatGPT-ähnlicher UI.
"""
from flask import Flask, render_template, request, jsonify
from src.weather import WeatherService
from src.news import NewsService
from src.nlp import NLPProcessor

app = Flask(__name__)


class WebKIAssistant:
    """Web-Version des KI-Assistenten."""

    def __init__(self):
        self.weather_service = WeatherService()
        self.news_service = NewsService()
        self.nlp = NLPProcessor()
        self.name = "KI-Assistent"

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
            return "👋 Auf Wiedersehen! Bis zum nächsten Mal."

        if intent == "greeting":
            return self._get_greeting()

        if intent == "help":
            return self._get_help()

        if intent == "weather":
            weather_data = self.weather_service.get_weather(parameter)
            return self.weather_service.format_weather(weather_data)

        if intent == "news":
            try:
                count = int(parameter) if parameter else 3
            except (ValueError, TypeError):
                count = 3
            news_data = self.news_service.get_top_news(count)
            return self.news_service.format_news(news_data)

        # Unbekannte Anfrage
        return """🤔 Das habe ich leider nicht verstanden.

Ich kann dir helfen bei:
• Wetterfragen: "Wie ist das Wetter heute?"
• Nachrichten: "Was sind die Top 3 News?"

Tippe 'hilfe' für mehr Informationen."""

    def _get_greeting(self) -> str:
        """Gibt eine Begrüßung zurück."""
        return f"""🤖 Hallo! Ich bin dein {self.name}.

Ich kann dir bei folgenden Dingen helfen:
• Wetterfragen (z.B. "Wie ist das Wetter heute?" oder "Wetter in München")
• Aktuelle Nachrichten (z.B. "Was sind die Top 3 News?")

Tippe 'hilfe' für weitere Informationen."""

    def _get_help(self) -> str:
        """Gibt die Hilfe-Nachricht zurück."""
        return """📚 Verfügbare Befehle:

🌤️ WETTER:
   • "Wie ist das Wetter?"
   • "Wetter in Berlin"
   • "Temperatur in München"

📰 NACHRICHTEN:
   • "Was gibt es Neues?"
   • "Top 3 News"
   • "Zeige mir 5 Nachrichten"

💡 Tipp: Stelle deine Fragen in natürlicher Sprache!"""


# Globale Instanz des Assistenten
assistant = WebKIAssistant()


@app.route("/")
def index():
    """Hauptseite mit Chat-Interface."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """API-Endpunkt für Chat-Nachrichten."""
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Bitte gib eine Nachricht ein."}), 400

    response = assistant.process_input(user_message)
    return jsonify({"response": response})


def main():
    """Startet den Webserver."""
    print("🚀 KI-Assistent Web-Interface startet auf http://localhost:10000")
    app.run(host="127.0.0.1", port=10000, debug=False)


if __name__ == "__main__":
    main()

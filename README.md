# KI-Assistent

Ein einfacher KI-Chatbot, der Wetter- und Nachrichtenfragen beantworten kann. Optimiert für den Betrieb in einem SUSE/openSUSE Container.

## Features

- 🌤️ **Wetterfragen**: "Wie ist das Wetter heute?" oder "Wetter in München"
- 📰 **Nachrichten**: "Was sind die Top 3 News?" oder "Zeige mir 5 Nachrichten"
- 🗣️ **Natürliche Sprache**: Versteht deutsche Fragen in natürlicher Formulierung
- 🐳 **Container-ready**: Dockerfile für openSUSE Leap enthalten

## Schnellstart mit Docker

### Mit Docker Compose (empfohlen)

```bash
# Repository klonen
git clone https://github.com/noahzuerii/KI.git
cd KI

# Optional: API-Keys konfigurieren
cp .env.example .env
# .env Datei bearbeiten und API-Keys eintragen

# Container bauen und starten
docker-compose up --build
```

### Mit Docker direkt

```bash
# Image bauen
docker build -t ki-assistant .

# Container starten (interaktiv)
docker run -it ki-assistant
```

## Lokale Entwicklung

### Voraussetzungen

- Python 3.9 oder höher
- pip

### Installation

```bash
# Repository klonen
git clone https://github.com/noahzuerii/KI.git
cd KI

# Virtuelle Umgebung erstellen (optional, aber empfohlen)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder: venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt

# Optional: .env Datei konfigurieren
cp .env.example .env
```

### Starten

```bash
python app.py
```

### Tests ausführen

```bash
python -m pytest tests/ -v
# oder
python -m unittest discover tests/
```

## Konfiguration

Die Anwendung kann über Umgebungsvariablen oder eine `.env` Datei konfiguriert werden:

| Variable | Beschreibung | Standard |
|----------|--------------|----------|
| `NEWSAPI_KEY` | API-Key für NewsAPI ([hier kostenlos holen](https://newsapi.org/)) | - |
| `DEFAULT_CITY` | Standard-Stadt für Wetterabfragen | Zürich |

**Hinweis**: Für Wetterdaten wird die kostenlose Open-Meteo API verwendet (kein API-Key erforderlich). Ohne NewsAPI-Key zeigt die Anwendung Demo-Nachrichten an.

## Projektstruktur

```
KI/
├── app.py              # Hauptanwendung
├── src/
│   ├── __init__.py
│   ├── config.py       # Konfiguration
│   ├── nlp.py          # Sprachverarbeitung
│   ├── news.py         # News-Service
│   └── weather.py      # Wetter-Service
├── tests/
│   ├── __init__.py
│   ├── test_nlp.py
│   ├── test_news.py
│   └── test_weather.py
├── Dockerfile          # Docker-Image für openSUSE
├── docker-compose.yml  # Docker Compose Konfiguration
├── requirements.txt    # Python Dependencies
└── .env.example        # Beispiel-Konfiguration
```

## Beispiel-Interaktion

```
🤖 Hallo! Ich bin dein KI-Assistent.

👤 Du: Wie ist das Wetter in München?

🤖 KI-Assistent: 🌤️ Wetter in München:
• Temperatur: 18.5°C (gefühlt: 17.2°C)
• Wetterlage: leicht bewölkt
• Luftfeuchtigkeit: 65%
• Wind: 3.5 m/s

👤 Du: Top 3 News

🤖 KI-Assistent: 📰 Top 3 Nachrichten:

1. Technologie-Update
   📍 Quelle: Tagesschau
   📝 Die neuesten Entwicklungen...
```

## Lizenz

Dieses Projekt steht unter der GNU General Public License v3.0 - siehe [LICENSE](LICENSE) für Details
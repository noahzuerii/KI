"""
News-Service für den KI-Assistenten.
Nutzt die NewsAPI.
"""
import requests
from .config import Config


class NewsService:
    """Service zum Abrufen von Nachrichten."""
    
    def __init__(self):
        self.api_key = Config.NEWSAPI_KEY
        self.api_url = Config.NEWS_API_URL
    
    def _is_api_key_valid(self) -> bool:
        """Prüft ob ein gültiger API-Key konfiguriert ist."""
        return self.api_key is not None and self.api_key != Config.API_KEY_PLACEHOLDER
    
    def get_top_news(self, count: int = 3, country: str = "de") -> dict:
        """
        Ruft die Top-Nachrichten ab.
        
        Args:
            count: Anzahl der Nachrichten (Standard: 3)
            country: Ländercode (Standard: de für Deutschland)
            
        Returns:
            Dictionary mit Nachrichten oder Fehlermeldung
        """
        if not self._is_api_key_valid():
            return self._get_demo_news(count)
        
        try:
            params = {
                "country": country,
                "pageSize": count,
                "apiKey": self.api_key
            }
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "ok":
                return {
                    "success": False,
                    "error": data.get("message", "Unbekannter API-Fehler")
                }
            
            articles = []
            for article in data.get("articles", [])[:count]:
                articles.append({
                    "title": article.get("title", "Kein Titel"),
                    "description": article.get("description", "Keine Beschreibung"),
                    "source": article.get("source", {}).get("name", "Unbekannt"),
                    "url": article.get("url", "")
                })
            
            return {
                "success": True,
                "articles": articles
            }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Fehler beim Abrufen der Nachrichten: {str(e)}"
            }
    
    def _get_demo_news(self, count: int) -> dict:
        """Gibt Demo-Nachrichten zurück wenn kein API-Key konfiguriert ist."""
        demo_articles = [
            {
                "title": "Beispiel-Nachricht 1: Technologie-Update",
                "description": "Die neuesten Entwicklungen in der Technologiebranche.",
                "source": "Demo News",
                "url": "https://example.com/news1"
            },
            {
                "title": "Beispiel-Nachricht 2: Wirtschaft aktuell",
                "description": "Aktuelle Wirtschaftsnachrichten und Markttrends.",
                "source": "Demo News",
                "url": "https://example.com/news2"
            },
            {
                "title": "Beispiel-Nachricht 3: Wissenschaft & Forschung",
                "description": "Neue Erkenntnisse aus der Wissenschaft.",
                "source": "Demo News",
                "url": "https://example.com/news3"
            }
        ]
        return {
            "success": True,
            "demo": True,
            "articles": demo_articles[:count]
        }
    
    def format_news(self, news_data: dict) -> str:
        """
        Formatiert Nachrichten als lesbaren Text.
        
        Args:
            news_data: Dictionary mit Nachrichtendaten
            
        Returns:
            Formatierter String mit Nachrichten
        """
        if not news_data.get("success"):
            return news_data.get("error", "Unbekannter Fehler")
        
        demo_note = ""
        if news_data.get("demo"):
            demo_note = "(Demo-Daten - Konfiguriere NEWSAPI_KEY für echte Nachrichten)\n\n"
        
        output = f"📰 Top {len(news_data['articles'])} Nachrichten:\n{demo_note}"
        
        for i, article in enumerate(news_data["articles"], 1):
            output += f"""
{i}. {article['title']}
   📍 Quelle: {article['source']}
   📝 {article['description'][:100]}{'...' if len(article['description']) > 100 else ''}
"""
        
        return output.strip()

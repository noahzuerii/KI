"""
Tests für das Web-Interface des KI-Assistenten.
"""
import unittest
from web_app import app, WebKIAssistant


class TestWebApp(unittest.TestCase):
    """Tests für die Flask Web-Anwendung."""

    def setUp(self):
        """Setup für jeden Test."""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page_loads(self):
        """Test ob die Hauptseite geladen wird."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'KI-Assistent', response.data)

    def test_chat_api_greeting(self):
        """Test der Chat-API mit Begrüßung."""
        response = self.app.post('/api/chat',
                                 json={'message': 'Hallo'},
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('response', data)
        self.assertIn('Hallo', data['response'])

    def test_chat_api_help(self):
        """Test der Chat-API mit Hilfe-Anfrage."""
        response = self.app.post('/api/chat',
                                 json={'message': 'hilfe'},
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('response', data)
        self.assertIn('Verfügbare Befehle', data['response'])

    def test_chat_api_empty_message(self):
        """Test der Chat-API mit leerer Nachricht."""
        response = self.app.post('/api/chat',
                                 json={'message': ''},
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_chat_api_weather(self):
        """Test der Chat-API mit Wetter-Anfrage."""
        response = self.app.post('/api/chat',
                                 json={'message': 'Wie ist das Wetter?'},
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('response', data)

    def test_chat_api_news(self):
        """Test der Chat-API mit News-Anfrage."""
        response = self.app.post('/api/chat',
                                 json={'message': 'Top 3 News'},
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('response', data)
        self.assertIn('Nachrichten', data['response'])


class TestWebKIAssistant(unittest.TestCase):
    """Tests für die WebKIAssistant-Klasse."""

    def setUp(self):
        """Setup für jeden Test."""
        self.assistant = WebKIAssistant()

    def test_process_greeting(self):
        """Test Begrüßungs-Verarbeitung."""
        response = self.assistant.process_input('Hallo')
        self.assertIn('Hallo', response)
        self.assertIn('KI-Assistent', response)

    def test_process_help(self):
        """Test Hilfe-Verarbeitung."""
        response = self.assistant.process_input('hilfe')
        self.assertIn('Verfügbare Befehle', response)

    def test_process_unknown(self):
        """Test unbekannte Anfrage."""
        response = self.assistant.process_input('xyz123')
        self.assertIn('nicht verstanden', response)


if __name__ == '__main__':
    unittest.main()

import requests
from bs4 import BeautifulSoup

def get_website_content(website_url=None):
    try:
        # Website-Inhalt abrufen
        response = requests.get(website_url)
        response.raise_for_status()  # Fehler abfangen, falls die Anfrage fehlschlägt
        html_content = response.text

        # Text aus dem HTML-Inhalt extrahieren
        soup = BeautifulSoup(html_content, 'html.parser')

        # Irrelevante HTML-Tags entfernen
        irrelevant_tags = ['script', 'style']  # Beispielhafte Liste von Tags, die entfernt werden sollen
        for tag in soup(irrelevant_tags):
            tag.extract()

        # Textinhalt extrahieren
        text_content = soup.get_text(separator=" ")
        # Entferne überflüssige Zeilenumbrüche, Platzhalter usw.
        text_content = " ".join(text_content.split())
        #print("text", text_content)
        return text_content
    
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Website-Inhalte: {e}")
        return None
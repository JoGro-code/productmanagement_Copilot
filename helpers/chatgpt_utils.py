import openai
from helpers.config import OPENAI_ORGANIZATION, OPENAI_API_KEY

openai.organization = OPENAI_ORGANIZATION
openai.api_key = OPENAI_API_KEY


def filter_completions(completions, product_text):
    filtered_completions = []
    for entry in completions:
        entry_type = entry[0]
        entry_content = entry[1].replace(product_text, "")
        filtered_entry = (entry_type, entry_content)
        filtered_completions.append(filtered_entry)
    return filtered_completions

def pass_to_chatgpt(website_content=None, company_name=None, product_name=None, product_text=None, default_temperature=0.6):
    completions = []
    messages = []

    question = f"Was sind die am wichtigsten Verkaufsargumente auf einer Produkt Landingpage für {product_name}, damit {company_name} eine hochkonvertierende Produktdetailseite hat."
    messages.append({"role": "user", "content": question})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5  
    )

    if response and response.choices:
        #completions.append(("Frage", question))
        completions.append(("Antwort", response.choices[0].message.content))
    else:
        return "Fehler beim Kommunizieren mit der ChatGPT-API."

    questions = [
        (f"Du bist Online Marketing Spezialist. Woran liegt es dass das Produkt nicht konvertiert? Hier ist die aktuelle Beschreibung: {product_name} {product_text}", 0.3, "Vorschläge für die Produktbeschreibung"),
        (f"Bewerte die oben genannte aktuelle Beschreibung für {product_name} mit einem Score von 0 für schlecht und 100 perfekt im Bezug auf Online Marketing. Gebe zwingend einen ZahlenWert zurück.Hier ist die aktuelle Beschreibung: {product_name} {product_text}", 0.1, "Online Marketing Score"),  
        (f"Was sind die Zielgruppen von {company_name} für das Produkt? Mache konkrete Vorschläge.", 0.5, "Zielgruppen"), 
        (f"Welche Informationen muss die Produktbeschreibung von oben genanntem {product_name} unbedingt enthalten um den experten der Zielgruppe im Vergleich zum Wettbewerb zu überzeugen? Mache konkrete Vorschläge.", 0.5), 
        (f"Optimiere für diese Zielgruppe die Produktbeschreibung für {product_name} zu den vorgeschlagenen Verbesserungen.", 0.8, "Beschreibung je Zielgruppe"),  
        (f"Basierend auf allgemeinem Wissen und deinem letzten Trainingsdatensatz und als Preismanagement-Experte, welche Preisspanne würdest du schätzen pro {product_name} im B2B-Bereich netto? Bitte gib eine allgemeine Einschätzung wenn keine spezifischen Daten vorhanden sind. Es muss eine konkrete Zahl oder einen niedrigen geschätzten Bereich in der Antwort vorhanden sein, auch wenn es sich nicht um aktuelle Daten handelt. Im Zweifel basierend auf typischen Preisen oder ähnlichen Produkten in der Branche", 0.2, "Pricing by JoGro AI"),  
        (f"Basierend auf deinem Trainingsdatensatz und in deiner Rolle als Preismanagement-Experte: Welche Preisspanne würdest du für {product_name} im B2B-Bereich netto schätzen? Bitte identifiziere die Hauptzielgruppen für dieses Produkt und gib für jede einen geschätzten niedrigen Preisbereich an. Falls du keine spezifischen Daten hast, stütze dich auf typische Preise oder ähnliche Produkte in der Branche. Die Antwort sollte nur die Form 'Zielgruppe: geschätzter Preisbereich' haben.", 0.3, "Custom Audience Pricing by JoGro AI"),  
        (f"Nenne die TOP-SEO-KEYWORDS für {product_name} und optimiere die Produktbeschreibung in der Tonalität je Zielgruppe.", 0.7, "KeyWords"),
        (f"Schreibe 5 Newsletter Headlines Anwendungsbezogen für {product_name} {product_text}.", 0.7, "Newsletter Topics"),
    ]
    i = 0
    for question, temperature, topic in questions:
        #print(question)
        
        messages = [{"role": "system", "content": website_content}]

        messages.append({"role": "user", "content": question})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature
        )

        if response and response.choices:
            #completions.append(("Thema"+ str(i), question))
            completions.append((f"Thema {i}", topic))
            completions.append(("Antwort", response.choices[0].message.content))
            i += 1
        else:
            return "Fehler beim Kommunizieren mit der ChatGPT-API."

    completions = filter_completions(completions, product_text)
    return completions
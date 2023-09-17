import openai
from config import OPENAI_ORGANIZATION, OPENAI_API_KEY

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
        completions.append(("Frage", question))
        completions.append(("Antwort", response.choices[0].message.content))
    else:
        return "Fehler beim Kommunizieren mit der ChatGPT-API."

    questions = [
        (f"Du bist Online Marketing Spezialist. Woran liegt es dass das Produkt nicht konvertiert? Hier ist die aktuelle Beschreibung: {product_name} {product_text}", 0.3),
        (f"Bewerte die oben genannte aktuelle Beschreibung für {product_name} mit einem Score von 0 für schlecht und 100 perfekt im Bezug auf Online Marketing. Gebe zwingend einen ZahlenWert zurück.Hier ist die aktuelle Beschreibung: {product_name} {product_text}", 0.1),  
        (f"Was sind die Zielgruppen von {company_name} für das Produkt? Mache konkrete Vorschläge.", 0.5), 
        (f"Optimiere für diese Zielgruppe die Produktbeschreibung für {product_name} zu den vorgeschlagenen Verbesserungen.", 0.8),  
        (f"Was wäre eine konkrete anzunehmende Preisspanne pro {product_name}, basierend auf den Dir zur Verfügung stehenden Daten im B2B Bereich und netto? Die Antwort muss eine Zahl enthalten. Mache einen direkten Vorschlag.", 0.2),  
        (f"Mache je von dir oben identifizierter Zielgruppe einen konkreten Preisvorschlag pro {product_name}. Die Antwort muss mindestens eine Zahl enthalten.", 0.3),  
        (f"Nenne die TOP-SEO-KEYWORDS für {product_name} und optimiere die Produktbeschreibung in der Tonalität je Zielgruppe.", 0.7),
        (f"Schreibe 5 Newsletter Headlines Anwendungsbezogen für {product_name} {product_text}.", 0.7),
    ]

    for question, temperature in questions:
        print(question)
        
        messages = [{"role": "system", "content": website_content}]

        messages.append({"role": "user", "content": question})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature
        )

        if response and response.choices:
            completions.append(("Frage", question))
            completions.append(("Antwort", response.choices[0].message.content))
        else:
            return "Fehler beim Kommunizieren mit der ChatGPT-API."

    completions = filter_completions(completions, product_text)
    return completions






#import openai
#
#openai.organization = "org-21h5UhX8KODhLjTZGGmYmuH5" #"OpenAI-Organization" #"org-21h5UhX8KODhLjTZGGmYmuH5"
#openai.api_key = "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"
#
##organization = "org-21h5UhX8KODhLjTZGGmYmuH5"
##api_key = "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"
#def pass_to_chatgpt(website_content=None, company_name=None, product_name=None, product_text=None, default_temperature=0.6):
#    completions = []
#    messages = []
#
#    question = f"Was sind die am wichtigsten Verkaufsargumente auf einer Produkt Landingpage für {product_name}, damit {company_name} eine hochkonvertierende Produktdetailseite hat."
#    messages.append({"role": "user", "content": question})
#
#    response = openai.ChatCompletion.create(
#        model="gpt-3.5-turbo",
#        messages=messages,
#        temperature=0.5  # Temperatur für Frage zu den wichtigsten Verkaufsargumenten
#    )
#
#    if response and response.choices:
#        completions.append(("Frage", question))
#        completions.append(("Antwort", response.choices[0].message.content))
#    else:
#        return "Fehler beim Kommunizieren mit der ChatGPT-API."
#
#    questions = [
#        (f"Woran liegt es dass das Produkt nicht konvertiert? Hier ist die aktuelle Beschreibung: {product_name} {product_text}", 0.3),
#        (f"Bewerte die oben genannte aktuelle Beschreibung für {product_name} mit einem Score von 0 für schlecht und 100 perfekt im Bezug auf Online Marketing. Gebe zwingend einen Wert zurück.Hier ist die aktuelle Beschreibung: {product_name} {product_text}", 0.1),  # Temperatur für Frage zur Bewertung der Produktbeschreibung
#        (f"Was sind die Zielgruppen von {company_name} für das Produkt? Mache konkrete Vorschläge.", 0.5),  # Temperatur für Frage zur Zielgruppe und konkreten Vorschlägen
#        (f"Optimiere für diese Zielgruppe die Produktbeschreibung für {product_name} zu den vorgeschlagenen Verbesserungen.", 0.8),  # Temperatur für Frage zur Optimierung der Produktbeschreibung
#        (f"Was wäre eine konkrete anzunehmende Preisspanne pro {product_name}, basierend auf den Dir zur Verfügung stehenden Daten im B2B Bereich und netto? Die Antwort muss eine Zahl enthalten. Mache einen direkten Vorschlag.", 0.2),  #Temperatur für Frage zur anzunehmenden Preisspanne
#        #("Berücksichtige B2B Bereich und netto für Preisvorschlage. Die Antwort muss mindestens eine Zahl enthalten.", 0.3),  # Temperatur für Frage zur Preisspanne im B2B-Bereich
#        (f"Mache je von dir oben identifizierter Zielgruppe einen konkreten Preisvorschlag pro {product_name}. Die Antwort muss mindestens eine Zahl enthalten.", 0.3),  # Temperatur für Frage zur Angabe von konkreten Preisvorschlägen
#        (f"Nenne die TOP-SEO-KEYWORDS für {product_name} und optimiere die Produktbeschreibung in der Tonalität je Zielgruppe.", 0.7),
#        (f"Schreibe 5 Newsletter Headlines Anwendungsbezogen für {product_name} {product_text}.", 0.7),
#    ]
#
#    for question, temperature in questions:
#        messages = [{"role": "system", "content": website_content}]
#
#        messages.append({"role": "user", "content": question})
#
#        response = openai.ChatCompletion.create(
#            model="gpt-3.5-turbo",
#            messages=messages,
#            temperature=temperature
#        )
#
#        if response and response.choices:
#            completions.append(("Frage", question))
#            completions.append(("Antwort", response.choices[0].message.content))
#        else:
#            return "Fehler beim Kommunizieren mit der ChatGPT-API."
#
#    return completions
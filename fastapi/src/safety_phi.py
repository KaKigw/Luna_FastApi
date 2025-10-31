import re
import spacy

# load lightweight NER
nlp = spacy.load("en_core_web_sm")

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"\+?\d[\d\s\-]{7,}\d")
DATE = re.compile(r"\b(?:\d{1,2}[/-])?\d{1,2}[/-]\d{2,4}\b")

def scrub_phi(text: str) -> str:
    # regex-based removal
    text = EMAIL.sub("[EMAIL]", text)
    text = PHONE.sub("[PHONE]", text)
    text = DATE.sub("[DATE]", text)

    # NER-based
    doc = nlp(text)
    out = []
    for ent in doc.ents:
        if ent.label_ in ("PERSON", "ORG", "GPE", "LOC"):
            text = text.replace(ent.text, f"[{ent.label_}]")
    return text


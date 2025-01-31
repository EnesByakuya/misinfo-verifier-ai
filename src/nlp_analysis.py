import spacy

def analyze_text(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

if __name__ == "__main__":
    sample_text = "COVID-19 was caused by 5G technology."
    print(analyze_text(sample_text))
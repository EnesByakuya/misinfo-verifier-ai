import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Tokenizes text, removes stopwords and punctuations, and performs lemmatization.
    Extracts named entities.
    """
    doc = nlp(text)

    # Remove stopwords and punctuation, and perform lemmatization
    clean_tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]

    # Named Entity Recognition (NER)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return {
        "clean_text": " ".join(clean_tokens),
        "entities": entities
    }

if __name__ == "__main__":
    sample_text = "5G technology is causing COVID-19, according to some conspiracy theories."
    result = preprocess_text(sample_text)
    print("Processed Text:", result["clean_text"])
    print("Named Entities:", result["entities"])

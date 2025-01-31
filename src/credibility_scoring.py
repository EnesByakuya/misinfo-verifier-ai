import re
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Example lists (Can be expanded)
UNRELIABLE_SOURCES = ["beforeitsnews.com", "infowars.com", "naturalnews.com"]
FACT_CHECK_SOURCES = ["snopes.com", "politifact.com", "factcheck.org"]
SENSATIONAL_WORDS = ["shocking", "unbelievable", "exposed", "hoax", "conspiracy", "fake", "evil"]

def calculate_credibility(article):
    """
    Assigns a credibility score (0-100) based on various factors.
    """

    # Extract entities and preprocess text
    doc = nlp(article["content"])
    words = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]

    score = 50  # Start with a neutral score

    # 1. Check source credibility
    for source in UNRELIABLE_SOURCES:
        if source in article["url"]:
            score -= 30  # Reduce credibility for unreliable sources

    for source in FACT_CHECK_SOURCES:
        if source in article["url"]:
            score += 20  # Increase credibility if it's from a fact-checking site

    # 2. Check for sensationalist words
    sensational_count = sum(1 for word in words if word in SENSATIONAL_WORDS)
    score -= sensational_count * 2  # Reduce score for each sensational word

    # 3. Check for uppercase words (indicates sensationalism)
    uppercase_count = sum(1 for word in words if word.isupper())
    score -= uppercase_count * 2  # Reduce for excessive uppercase

    # 4. Check for factual claims (basic heuristic)
    fact_related_words = ["study", "research", "scientist", "evidence", "confirmed"]
    fact_count = sum(1 for word in words if word in fact_related_words)
    score += fact_count * 2  # Increase for factual language

    # Ensure score stays within 0-100
    score = max(0, min(100, score))

    return {"title": article["title"], "url": article["url"], "score": score}

if __name__ == "__main__":
    test_article = {
        "title": "5G is causing a global pandemic!",
        "url": "http://fake-news.com/5g-pandemic",
        "content": "Scientists have uncovered a shocking conspiracy. 5G is dangerous and spreading COVID-19!"
    }

    result = calculate_credibility(test_article)
    print("Credibility Score:", result["score"])

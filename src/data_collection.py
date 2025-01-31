import requests
import psycopg2
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pickle
import time
from .train_model import vectorizer

# Load trained model
model = pickle.load(open("fake_news_model.pkl", "rb"))
# Load environment variables from .env file
load_dotenv()

# NewsAPI configuration
NEWSAPI_KEY = "a6a72ce046974cc681809e3f6ac2fc7f"
NEWSAPI_URL = "https://newsapi.org/v2/everything"

# Database connection function
def get_db_connection():
    """
    Establishes and returns a database connection.
    """
    try:
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
    except Exception as e:
        print("Database connection failed:", e)
        return None


# Function to check if a query already exists in the database
def query_exists(query):
    """
    Checks if the given search query already exists in the database.
    """
    conn = get_db_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM articles WHERE query = %s", (query,))
    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count > 0


# Function to extract full article content from a URL
def fetch_article_content(url):
    """
    Extracts the full text from a given news article URL using BeautifulSoup.
    """
    try:
        response = requests.get(url, timeout=10)  # Timeout prevents infinite waits
        if response.status_code != 200:
            print(f"Failed to fetch article from {url}: {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')

        if not paragraphs:  # If no readable content is found, return None
            print(f"No readable content found at {url}")
            return None

        full_text = ' '.join([para.get_text() for para in paragraphs])
        return full_text.strip()

    except requests.exceptions.RequestException as e:
        print(f"Request error for {url}: {e}")
        return None


def predict_credibility(text):
    """
    Predicts the credibility of an article using the trained model.
    """
    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)[0]
    return "Fake" if prediction == 1 else "Real"


def fetch_articles(query, retries=3, delay=2):
    """
    Fetches articles related to the query from NewsAPI.
    Implements retry logic for connection issues.
    """
    params = {
        "q": query,
        "apiKey": NEWSAPI_KEY,
        "pageSize": 10,  # Fetch up to 10 articles
        "language": "en"  # Filter by English articles
    }

    for attempt in range(retries):
        try:
            response = requests.get(NEWSAPI_URL, params=params, timeout=10)  # Set timeout to 10 seconds
            response.raise_for_status()  # Raise an exception for HTTP errors
            articles = response.json().get("articles", [])

            processed_articles = []
            for article in articles:
                title = article.get("title", "")
                url = article.get("url", "")
                full_text = fetch_article_content(url)

                if full_text:
                    credibility = predict_credibility(full_text)  # Get credibility score
                    processed_articles.append((title, url, full_text, credibility))

            return processed_articles if processed_articles else None

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                return None


# Function to store search results in the PostgreSQL database
def save_to_db(articles, query):
    """Save collected articles into PostgreSQL database."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        for title, url, content, credibility in articles:
            cur.execute("""
                INSERT INTO articles (query, title, url, content, credibility) 
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING;
            """, (query, title, url, content, credibility))

        conn.commit()
        cur.close()
        conn.close()
        print("Data saved successfully.")
    except Exception as e:
        print(f"Database error: {e}")


# Main execution flow
if __name__ == "__main__":
    query = input("Enter search term: ")

    if query_exists(query):
        print(f"'{query}' has already been searched. Fetching from database instead.")
    else:
        results = fetch_articles(query)

        if results:
            for title, link, _, credibility in results[:5]:  # Show top 5 results
                print(f"{title} - {link} - {credibility}")
            save_to_db(results, query)
        else:
            print("No results found.")
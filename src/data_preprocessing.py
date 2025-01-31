import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Path to dataset folder from environment variable
FAKENEWSNET_PATH = os.getenv("FAKENEWSNET_PATH")

def load_fake_news_data():
    """
    Loads FakeNewsNet dataset from CSV files and extracts relevant fields.
    """
    datasets = ["gossipcop_fake", "gossipcop_real", "politifact_fake", "politifact_real"]
    dataframes = []

    for dataset in datasets:
        file_path = os.path.join(FAKENEWSNET_PATH, f"{dataset}.csv")
        df = pd.read_csv(file_path)
        label = 1 if "fake" in dataset else 0
        df["label"] = label
        dataframes.append(df)

    # Combine all datasets
    df = pd.concat(dataframes, ignore_index=True)

    # Check if required columns exist
    required_columns = ["title", "news_url", "tweet_ids", "label"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Missing columns in the dataset: {missing_columns}")

    # Keep only necessary columns
    df = df[required_columns].dropna()

    # Combine title and tweet_ids
    df["article"] = df["title"] + " " + df["tweet_ids"]

    return df[["article", "label"]]

if __name__ == "__main__":
    df = load_fake_news_data()
    print(df.head())
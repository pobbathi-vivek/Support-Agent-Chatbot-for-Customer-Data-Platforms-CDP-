import requests
from bs4 import BeautifulSoup
import re
import chromadb
import ollama

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db_segment_data")  # Persistent storage
collection = chroma_client.get_or_create_collection(name="web_scrape_data")

cnt = 0  # Global counter for successful scrapes

def scrape_url(url):
    """Fetches and cleans text from a webpage."""
    global cnt  # Use the global counter
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            cleaned_text = clean_text(text)
            if len(cleaned_text) > 100:  # Ensuring meaningful data is present
                cnt += 1  # Increment count for successful scrapes
                print(f"Successfully scraped {cnt} URLs")
                return cleaned_text
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return None

def clean_text(text):
    """Cleans the extracted text."""
    text = text.encode('ascii', 'ignore').decode('ascii')  # Normalize Unicode
    text = re.sub(r'\S+@\S+', '', text)  # Remove emails
    text = re.sub(r'[^\w\s.,!?]', '', text)  # Remove special characters
    text = re.sub(r'\d+', '', text)  # Remove numbers
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize spaces
    return text

def generate_embedding(text):
    """Generates an embedding using Ollama."""
    try:
        response = ollama.embeddings(model="mistral", prompt=text)  # Change model if needed
        return response['embedding'] if 'embedding' in response else None
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def save_to_vector_db(url, text):
    """Generates embeddings and saves URL & text in the vector database."""
    embedding = generate_embedding(text)
    if embedding:
        collection.add(
            ids=[url],  # Use URL as unique ID
            embeddings=[embedding],
            metadatas=[{"url": url, "text": text}]
        )
        print(f"Saved to DB: {url}")

# Read URLs from file and scrape content
with open("sublinks_segment.txt", "r") as file:
    urls = file.read().splitlines()

# Scrape and store data
for url in urls:
    scraped_text = scrape_url(url)
    if scraped_text:
        save_to_vector_db(url, scraped_text)

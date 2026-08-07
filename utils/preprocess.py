import re
import nltk
from nltk.corpus import stopwords

# Download stopwords only once
nltk.download("stopwords", quiet=True)

stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove punctuation, numbers, and special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Split into words
    words = text.split()

    # Remove stopwords
    words = [word for word in words if word not in stop_words]

    # Join back into a string
    return " ".join(words)
import pandas as pd
import os
import csv
from langdetect import detect
from googletrans import Translator
from textblob import TextBlob
import re

# --- CONFIG ---
INPUT_CSV = "notebooks/data/tatamotors_telegram_messages.csv"
OUTPUT_CSV = "notebooks/data/tatamotors_telegram_sentiment.csv"

# Load csv robustly
try:
    df = pd.read_csv(INPUT_CSV, sep=',', quoting=csv.QUOTE_ALL, engine='python', on_bad_lines="skip")
except Exception as e:
    print("CSV failed to load:", e)
    raise

# Check for 'message' column
if "message" not in df.columns:
    raise ValueError("CSV must have a 'message' column")

# Filter for safari or harrier comments (case-insensitive)
df = df[df['message'].str.contains('safari|harrier', case=False, na=False)].reset_index(drop=True)

# Text normalization function
def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r"[^a-z\s]", "", text)  # Remove special characters and digits
    text = re.sub(r"\s+", " ", text)  # Remove multiple spaces
    return text

# Normalize messages to create cleaned_message column
df['cleaned_message'] = df['message'].apply(normalize_text)

# Exclude generic greetings and boilerplate messages
exclude_keywords = ['hey there', 'welcome to', 'hello', 'thanks for joining']
pattern = '|'.join(exclude_keywords)
df_filtered = df[~df['cleaned_message'].str.contains(pattern, case=False)]

# Initialize translator
translator = Translator()

languages = []
translated_texts = []
sentiments = []

for txt in df_filtered['message']:
    try:
        lang = detect(txt)
    except:
        lang = "unknown"
    languages.append(lang)

    if lang == "hi":
        try:
            translated = translator.translate(txt, src='hi', dest='en').text
        except:
            translated = txt
    else:
        translated = txt
    translated_texts.append(translated)

    polarity = TextBlob(translated).sentiment.polarity
    if polarity > 0.1:
        sentiments.append("Positive")
    elif polarity < -0.1:
        sentiments.append("Negative")
    else:
        sentiments.append("Neutral")

df_filtered['language'] = languages
df_filtered['translated_message'] = translated_texts
df_filtered['sentiment'] = sentiments

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df_filtered.to_csv(OUTPUT_CSV, index=False)
print(f"Saved sentiment analysis results for {len(df_filtered)} comments to {OUTPUT_CSV}")

print("Sentiment counts:")
print(df_filtered['sentiment'].value_counts())

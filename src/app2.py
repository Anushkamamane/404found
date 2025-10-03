import pandas as pd
import os
import csv
from langdetect import detect
from googletrans import Translator
from textblob import TextBlob

# --- CONFIG ---
INPUT_CSV = "notebooks/data/reddit_comments.csv"
OUTPUT_CSV = "notebooks/data/reddit_comments_sentiment.csv"

# Robustly load CSV with quoting
try:
   df = pd.read_csv(INPUT_CSV, sep=',', quoting=csv.QUOTE_ALL, engine='python', on_bad_lines="skip")

except Exception as e:
    print("CSV failed to load:", e)
    raise

print(df.head())

if "comment" not in df.columns:
    raise ValueError("CSV must have a 'comment' column")

# Initialize translator
translator = Translator()

# Prepare lists for new columns
languages = []
translated_texts = []
sentiments = []

for txt in df['comment']:
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

# Save results
df['language'] = languages
df['translated_comment'] = translated_texts
df['sentiment'] = sentiments

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False)
print(f"Saved sentiment analysis results for {len(df)} comments to {OUTPUT_CSV}")

print(df['sentiment'].value_counts())

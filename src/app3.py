import pandas as pd
import os
import csv
from langdetect import detect
from googletrans import Translator
from textblob import TextBlob
import re
from collections import Counter
from nrclex import NRCLex

# --- CONFIG ---
INPUT_CSV = "notebooks/data/tatamotors_telegram_messages.csv"
OUTPUT_CSV = "notebooks/data/tatamotors_telegram_sentiment.csv"
EMOTION_CSV = "notebooks/data/tatamotors_telegram_emotion.csv"
KEYWORDS_CSV = "notebooks/data/telegram_trending_keywords.csv"

# Load csv robustly
df = pd.read_csv(INPUT_CSV, sep=',', quoting=csv.QUOTE_ALL, engine='python', on_bad_lines="skip")
if "message" not in df.columns:
    raise ValueError("CSV must have a 'message' column")

# Filter for safari or harrier comments (case-insensitive)
df = df[df['message'].str.contains('safari|harrier', case=False, na=False)].reset_index(drop=True)

# Text normalization function
def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text

df['cleaned_message'] = df['message'].apply(normalize_text)

exclude_keywords = ['hey there', 'welcome to', 'hello', 'thanks for joining']
pattern = '|'.join(exclude_keywords)
df_filtered = df[~df['cleaned_message'].str.contains(pattern, case=False)].reset_index(drop=True)

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

# --- Sentiment Output ---
df_filtered['language'] = languages
df_filtered['translated_message'] = translated_texts
df_filtered['sentiment'] = sentiments

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df_filtered.to_csv(OUTPUT_CSV, index=False)
print(f"Saved sentiment analysis results for {len(df_filtered)} comments to {OUTPUT_CSV}")

# --- NRC Emotion Full Output ---
emotion_categories = ['fear', 'anger', 'anticipation', 'trust', 'surprise',
                     'positive', 'negative', 'sadness', 'disgust', 'joy']

emotion_rows = []
for idx, row in df_filtered.iterrows():
    msg = row['cleaned_message']
    nrc = NRCLex(str(msg))
    scores = nrc.raw_emotion_scores
    total = sum(scores.values()) if scores else 1
    norm_scores = {emo: scores.get(emo, 0) / total if total > 0 else 0 for emo in emotion_categories}
    out_row = {'index': idx, 'message': row['message']}
    out_row.update(norm_scores)
    emotion_rows.append(out_row)

emotions_df = pd.DataFrame(emotion_rows)
emotions_df.to_csv(EMOTION_CSV, index=False)
print(f"Saved full emotion analysis for {len(emotions_df)} comments to {EMOTION_CSV}")

# --- Trending Keywords Extraction (as before) ---
candidate_keywords = [
    'design', 'safety', 'mileage', 'comfort', 'price', 'features',
    'space', 'performance', 'service', 'technology'
]

keyword_stats = {k: {'Positive': 0, 'Negative': 0, 'Neutral': 0} for k in candidate_keywords}

for idx, row in df_filtered.iterrows():
    msg = row['cleaned_message']
    sentiment = row['sentiment']
    for kw in candidate_keywords:
        if kw in msg:
            keyword_stats[kw][sentiment] += 1

keyword_df = pd.DataFrame([
    {'keyword': k, 'Positive': v['Positive'], 'Negative': v['Negative'], 'Neutral': v['Neutral'],
     'Total': v['Positive'] + v['Negative'] + v['Neutral']}
    for k, v in keyword_stats.items()
]).sort_values(by='Total', ascending=False)

keyword_df.to_csv(KEYWORDS_CSV, index=False)
print(f"Saved trending keywords to {KEYWORDS_CSV}")
